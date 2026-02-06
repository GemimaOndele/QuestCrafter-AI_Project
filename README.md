# QuestCrafter-AI_Project

QuestCrafter is a lightweight generative AI project that builds a "Dungeon Master"
for RPG quests. It fine-tunes a small language model on curated prompt-to-quest
data, compares baseline vs fine-tuned outputs, evaluates quality with automatic
metrics and a human rubric, and delivers a simple interactive demo (Streamlit or
Gradio).

## Setup

- Python 3.10+
- Create a virtual env and install dependencies:
  - `pip install -r requirements.txt`

## Repository structure (W1)

- `data/` raw and processed datasets
- `dataset/` small tracked samples and metadata
- `scripts/` data and training scripts (W1 starts with `download_data.py`)
- `models/` model checkpoints (later)
- `docs/` project docs (board, roles)
- `notebooks/` analysis notebooks

## Data pipeline (W1)

We use the TinyStories dataset from Hugging Face. The script cleans, filters,
splits, and exports JSONL files with a consistent schema.

### Download + preprocess

Example:
`python download_data.py --dataset tinystories`

If you use local CSVs:
`python download_data.py --dataset tinystories --local_csv path/to/train.csv`

Output:
`data/raw/tinystories/train.jsonl`, `val.jsonl`, `test.jsonl`

### JSONL schema

Each line has:

- `prompt`
- `response`
- `source`
- optional `metadata` (e.g., `score`, `author`)

### Filters (defaults)

- Prompt: 5 to 300 characters (if prompt exists)
- Response: 20 to 800 characters
- Drops `[deleted]` / `[removed]`

Override with:
`--min_prompt_chars`, `--max_prompt_chars`, `--min_response_chars`, `--max_response_chars`, `--keep_deleted`

### TinyStories QA thresholds (report)

We document the following filtering rules for TinyStories QA:

- Keep stories between 50 and 300 tokens
- Drop empty or malformed entries
- Drop excessive repetition (same sentence 3+ times)

### Dataset stats (current splits)

Quick stats computed on the current JSONL splits (`data/raw/tinystories`):

- Train: 386 samples, avg 131.58 tokens, min 61, max 170
- Validation: 48 samples, avg 130.15 tokens, min 82, max 156
- Test: 49 samples, avg 131.90 tokens, min 79, max 157

Full details: `docs/dataset_stats.md`

Recompute:
`python scripts/compute_dataset_stats.py --input_dir data/raw --dataset tinystories --output docs/dataset_stats.md`

## Training-ready data (W3)

Convert JSONL splits to a single `text` field for HF Trainer:

Example:
`python scripts/prepare_training_data.py --input_dir data/raw --dataset tinystories --output_dir data/processed`

Optional control fields (W4, if used):
`python scripts/prepare_training_data.py --input_dir data/raw --dataset tinystories --output_dir data/processed --control_keys level,setting,tone`

## Evaluation scaffold (W4)

Compute simple lexical metrics for generated outputs:
`python scripts/evaluate_outputs.py --baseline outputs/baseline.jsonl --tuned outputs/tuned.jsonl --report outputs/metrics.json`

Compare baseline vs tuned (top-N by length delta):
`python scripts/compare_outputs.py --baseline outputs/baseline.jsonl --tuned outputs/tuned.jsonl --output outputs/compare_outputs.csv --top_n 20`

## Human rubric (W4)

Rubric template: `docs/human_rubric.md`

Build a CSV sheet to score baseline vs tuned:
`python scripts/build_human_eval_sheet.py --baseline outputs/baseline.jsonl --tuned outputs/tuned.jsonl --output docs/human_eval_template.csv`

Notebook: `notebooks/human_eval.ipynb`

Data volume note: human evaluation is more reliable with many scored prompts.
Aim for dozens to hundreds of rows, and if possible multiple evaluators.

## Real baseline/tuned generation (W4)

Generate outputs from a small model (baseline) or your tuned model:
`python scripts/generate_outputs.py --input data/raw/tinystories/test.jsonl --output outputs/baseline.jsonl --model_id distilgpt2`
`python scripts/generate_outputs.py --input data/raw/tinystories/test.jsonl --output outputs/tuned.jsonl --model_id YOUR_TUNED_MODEL_ID`

If prompts are empty, the script falls back to the `response` field.

## Team docs

- GitHub board and issues: `docs/github_board.md`
- Roles, branches, and tasks: `docs/team_roles.md`
- Sample outputs: `docs/sample_outputs.md`
- Project brief: `docs/source_project_brief.pdf`
- Day 1 summary: `docs/source_day1_summary.pdf`

## Upload dataset to Hugging Face

Use the script below to upload `archive.zip` to your dataset repo.

1) Install deps:
`pip install -r requirements.txt`

2) Upload (choose one):

- With token env:
`set HF_TOKEN=your_token`
`python upload_to_hf.py --repo_id GemimaOndele/questcrafter-dataset --file "C:\Users\gemim\OneDrive\Bureau\M1-cours-Data engineer\MSC 1 AI\Semestre 2\Foundations of machine learning and datascience\Project\archive.zip"`

- With token argument:
`python upload_to_hf.py --token your_token --repo_id GemimaOndele/questcrafter-dataset --file "C:\Users\gemim\OneDrive\Bureau\M1-cours-Data engineer\MSC 1 AI\Semestre 2\Foundations of machine learning and datascience\Project\archive.zip"`

If you already logged in with `huggingface-cli login`, the script will use that cached token.
