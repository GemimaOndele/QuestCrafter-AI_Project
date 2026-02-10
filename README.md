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
- `scripts/` data and training scripts (W1 starts with `download_data.py`)
- `models/` model checkpoints (later)
- `docs/` project docs (board, roles)

## Data pipeline (W1)
We filtered TinyStories to remove extremely short, overly long, and repetitive samples. Only stories between 50 and 300 tokens were kept, ensuring each example contains meaningful narrative structure while remaining efficient for training and evaluation.

We use the TinyStories dataset, filtered for quality and formatted into
instruction → response pairs. The dataset is split into train/validation/test
(80/10/10) with a fixed random seed for reproducibility.


## Evaluation (W2)
Model evaluation is performed using a fixed set of 50 quest prompts and a human
scoring rubric to ensure fair comparison between baseline and fine-tuned models.

### Test prompts
A fixed prompt set covering multiple settings, difficulty levels (1–10), tones,
and output lengths is stored in `evaluation/test_prompts.jsonl`. The same prompts
are reused across all models for reproducibility.

### Human rubric
Generated quests are scored on a 1–5 scale using three criteria:
- **Coherence**: Logical and well-structured narrative
- **Prompt faithfulness**: Adherence to level, setting, and tone
- **Creativity**: Originality and engaging content

Human evaluation complements automatic metrics by capturing qualitative aspects
of generation quality.


### Download + preprocess
Example:
`python download_data.py --dataset redditjokes --local_csv path/to/reddit_jokes.csv`

Output:
`data/raw/redditjokes/train.jsonl`, `val.jsonl`, `test.jsonl`

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

## Team docs
- GitHub board and issues: `docs/github_board.md`
- Roles, branches, and tasks: `docs/team_roles.md`
