## GitHub Project board (ready to use)

### Columns
1) Backlog
2) Ready
3) In Progress
4) Review
5) Done

### Labels to create
`data` `modeling` `evaluation` `demo` `docs` `infra`

### Issues (create and assign)
W1
- `DATA-1` Collect Reddit Jokes CSV and document source (label: data)
- `DATA-2` Implement cleaning + filters in `download_data.py` (label: data)
- `DATA-3` Train/val/test split + JSONL export (label: data)
- `DATA-4` Dataset stats + summary (label: data, docs)
- `DOC-1` Update README with pipeline usage (label: docs)

W2
- `EVAL-1` Define fixed test prompts (50+) (label: evaluation)
- `EVAL-2` Draft human rubric (coherence, creativity, faithfulness) (label: evaluation)
- `BASE-1` Baseline generation script (distilgpt2) (label: modeling)
- `BASE-2` Baseline failure analysis examples (label: evaluation)

W3
- `TRAIN-1` Fine-tuning script (HF Trainer) (label: modeling)
- `TRAIN-2` Track training curves + save checkpoint (label: modeling)

W4
- `CTRL-1` Add control tokens or fields (level/setting/tone) (label: modeling)
- `EVAL-3` Baseline vs fine-tuned evaluation report (label: evaluation)
- `SAFE-1` Add basic safety/length filters (label: evaluation)

W5
- `DEMO-1` Build Streamlit/Gradio demo (label: demo)
- `DOC-2` Final report (4-8 pages) (label: docs)
- `DOC-3` Presentation slides (label: docs)

### Suggested board setup
- Put all W1 items into Backlog
- Move current week items to Ready
- Only move to Review after a PR is open
