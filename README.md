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
We use the Reddit Jokes dataset (CSV). The script cleans, filters, splits, and
exports JSONL files with a consistent schema.

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
