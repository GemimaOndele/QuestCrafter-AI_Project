# 🧭 QuestCrafter‑AI Project (✨ Full Project Report)

[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/GemimaOndele/QuestCrafter-AI_Project)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://github.com/GemimaOndele/QuestCrafter-AI_Project)
[![Data](https://img.shields.io/badge/dataset-TinyStories-orange.svg)](https://github.com/GemimaOndele/QuestCrafter-AI_Project)
[![Branch](https://img.shields.io/badge/branches-data%20%7C%20training%20%7C%20evaluation%20%7C%20demo-purple.svg)](https://github.com/GemimaOndele/QuestCrafter-AI_Project)

QuestCrafter is a lightweight generative AI project that builds a **“Dungeon Master”**
for RPG quests. The project delivers a complete pipeline: data ingestion and
cleaning, training‑ready formatting, baseline vs fine‑tuning generation, human
and automatic evaluation, and a demo (Streamlit/Gradio).

```text
  🧱  DATA  ──▶  🧠  MODEL  ──▶  ✅  EVAL  ──▶  🎛️  DEMO
  clean/split      baseline+FT     rubric+plots     UI app
```

---

## 📌 Table of Contents

- Contributors
- Project Snapshot
- Architecture Map
- Repository Structure
- Branch Reports (Owners)
- Data Pipeline (W1)
- Training (W3)
- Evaluation (W4)
- Team Docs
- Setup

---

## 👥 Contributors

- **Gemima Ondele** — data lead (`feat/data-pipeline`)
- **Kachallah Fatima** — evaluation lead (`feat/evaluation`)
- **Mike‑Brady Mbolim Mbock** — modeling lead (`feat/training`)
- **Joseph Fabrice TSAPFACK** — demo lead (`feat/demo`)

---

## 🎯 Project Goals

| Goal | Description |
| --- | --- |
| Data quality | Filter and split TinyStories with clear QA thresholds |
| Modeling | Baseline generation + fine‑tuning with HF Transformers |
| Evaluation | Human rubric + automatic metrics |
| Delivery | Clear docs + demo app |

---

## 🧩 Project Snapshot

| Layer | Goal | Key Outputs |
| --- | --- | --- |
| 🧱 Data | Clean + split TinyStories | JSONL splits + stats |
| 🧠 Modeling | Baseline + fine‑tune | `distilgpt2` outputs |
| ✅ Evaluation | Human + metrics | Rubric, plots, reports |
| 🎛️ Demo | Interactive app | Streamlit/Gradio UI |

---

## 🗺️ Architecture Map

```text
flowchart LR
    A[TinyStories\n(HF dataset)] --> B[download_data.py\nclean + split]
    B --> C[data/raw/tinystories\ntrain/val/test.jsonl]
    C --> D[prepare_training_data.py\ntraining-ready text]
    D --> E[training/train_model.py\nfine-tune]
    C --> F[training/baseline_generation.py\nbaseline outputs]
    F --> G[outputs/*.jsonl]
    E --> G
    G --> H[docs/human_eval_template.csv]
    H --> I[notebooks/human_eval.ipynb\nanalysis + plots]
```

---

## 📁 Repository Structure

| Folder | Purpose |
| --- | --- |
| `data/` | Raw + processed datasets (ignored by git) |
| `dataset/` | Small tracked samples and metadata |
| `scripts/` | Data, evaluation, and utility scripts |
| `training/` | Baseline + fine‑tuning scripts |
| `outputs/` | Example generation outputs |
| `docs/` | Project docs, reports, assets |
| `notebooks/` | Analysis notebooks |

---

## 🧾 Branch Reports (Owners)

### `feat/data_pipeline` — **Gemima Ondele**

#### Goal (Data Pipeline)

Build a full TinyStories data pipeline, from ingestion to JSONL export, with
schema validation, statistics, and documentation.

#### Architecture & Flow (Data Pipeline)

1) **Ingestion + cleaning**  
   - Primary source: TinyStories (Hugging Face).
   - Length filtering and invalid entry removal.
2) **Normalization**  
   - Uniform schema: `prompt`, `response`, `source`, optional `metadata`.
3) **Splitting**  
   - Reproducible `train/val/test` splits.
4) **Quality checks**  
   - Schema and type validation.
   - Documented QA thresholds (50–300 tokens).
5) **Export + stats**  
   - JSONL splits + Markdown stats report.

#### Key files (Data Pipeline)

- Pipeline: `download_data.py`
- Stats: `scripts/compute_dataset_stats.py` → `docs/dataset_stats.md`
- Training prep: `scripts/prepare_training_data.py`
- JSONL helpers: `scripts/jsonl_utils.py`

#### Outputs (Data Pipeline)

- `data/raw/tinystories/{train,val,test}.jsonl`
- `docs/dataset_stats.md`
- `docs/human_rubric.md`
- `docs/human_eval_template.csv`

---

### `feat/training` — **Mike‑Brady Mbolim Mbock**

#### Goal (Training)

Provide baseline generation and fine‑tuning scripts, plus example outputs for
evaluation.

#### Architecture & Flow (Training)

1) **Baseline generation**  
   - Load `distilgpt2`.
   - Generate from prompts (fallback to `response` if prompt is empty).
2) **Fine‑tuning**  
   - Build training texts (prompt + response).
   - Train with `Trainer` (HF Transformers).
3) **Export outputs**  
   - JSONL outputs for evaluation.

#### Key files (Training)

- Baseline: `training/baseline_generation.py`
- Fine‑tuning: `training/train_model.py`
- Outputs: `outputs/baseline.jsonl`, `outputs/finetuned.jsonl`,
  `outputs/baseline_test.jsonl`

---

## 🧪 Data Pipeline (W1)

**Dataset:** TinyStories (Hugging Face)  
**Schema:** `prompt`, `response`, `source`, optional `metadata`

### Example command

`python download_data.py --dataset tinystories`

Example summary (for reports):
> We filtered TinyStories to remove extremely short, overly long, or repetitive
> samples. Final stories range between **50–300 tokens**, ensuring concise but
> coherent training examples.

### Outputs

`data/raw/tinystories/train.jsonl`, `val.jsonl`, `test.jsonl`

### QA thresholds

- Keep stories between **50 and 300 tokens**
- Drop empty or malformed entries
- Drop excessive repetition (same sentence ≥ 3 times)

### Dataset stats (current splits)

| Split | Samples | Avg tokens | Min | Max |
| --- | --- | --- | --- | --- |
| Train | 386 | 131.58 | 61 | 170 |
| Validation | 48 | 130.15 | 82 | 156 |
| Test | 49 | 131.90 | 79 | 157 |

Recompute:
`python scripts/compute_dataset_stats.py --input_dir data/raw --dataset tinystories --output docs/dataset_stats.md`

---

## 🧠 Training (W3)

Prepare training text:
`python scripts/prepare_training_data.py --input_dir data/raw --dataset tinystories --output_dir data/processed`

Optional control fields:
`python scripts/prepare_training_data.py --input_dir data/raw --dataset tinystories --output_dir data/processed --control_keys level,setting,tone`

---

## ✅ Evaluation (W4)

Automatic metrics:
`python scripts/evaluate_outputs.py --baseline outputs/baseline.jsonl --tuned outputs/tuned.jsonl --report outputs/metrics.json`

Compare baseline vs tuned:
`python scripts/compare_outputs.py --baseline outputs/baseline.jsonl --tuned outputs/tuned.jsonl --output outputs/compare_outputs.csv --top_n 20`

Human rubric:

- Template: `docs/human_rubric.md`
- CSV: `docs/human_eval_template.csv`
- Notebook: `notebooks/human_eval.ipynb`

**Important:** human evaluation needs **lots of data**.  
Aim for **dozens to hundreds of scored rows**, ideally with multiple evaluators.

Quick example (CSV row):
`"prompt","baseline","tuned",3,4,3,4,"notes","evaluator","2026-02-06"`

---

## 📚 Team Docs

- GitHub board and issues: `docs/github_board.md`
- Roles, branches, and tasks: `docs/team_roles.md`
- Sample outputs: `docs/sample_outputs.md`
- Project brief: `docs/source_project_brief.pdf`
- Day 1 summary: `docs/source_day1_summary.pdf`

---

## 🛠️ Setup

- Python 3.10+
- `pip install -r requirements.txt`
