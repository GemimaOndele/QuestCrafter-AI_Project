# QuestCrafter-AI_Project

QuestCrafter is a lightweight generative AI system designed to function as a miniature “Dungeon Master” for RPG-style quest generation. The project fine-tunes a small language model on curated fantasy prompt-to-quest data derived from the TinyStories dataset, compares baseline and fine-tuned outputs, evaluates generation quality using both automatic and human metrics, and provides an interactive demo interface.

---

## Setup

### Requirements
- Python 3.10+
- Virtual environment recommended

### Installation

```bash
pip install -r requirements.txt
```

---

## Repository Structure

- `data/` – Raw and processed datasets  
- `scripts/` – Data preprocessing and training scripts  
- `models/` – Model checkpoints  
- `evaluation/` – Test prompts, evaluation scripts, and scoring files  
- `docs/` – Project documentation  

---

# Data Pipeline (W1)

## Dataset

The project uses the **TinyStories dataset**, selected for its short, narrative-driven structure suitable for fantasy quest generation.

## Filtering Strategy

To improve training quality, we applied the following preprocessing steps:

- Removed extremely short samples  
- Removed overly long samples  
- Removed repetitive or degenerate outputs  
- Retained stories between **50–300 tokens**

This ensures meaningful narrative structure, efficient training sequence length, and reduced noise during fine-tuning.

## Data Formatting

Each example is converted into an:

```
instruction → response
```

format where:

- `instruction` = structured quest prompt  
- `response` = target quest narrative  

## Data Splits

- 80% Training  
- 10% Validation  
- 10% Test  

A fixed random seed ensures reproducibility.

---

# Evaluation (W2–W4)

Evaluation compares the baseline model (`distilgpt2`) and the fine-tuned QuestCrafter model using both automatic and human-centered metrics. All evaluations are conducted on a fixed set of 50 structured prompts.

---

## Test Prompt Set

Stored in:

```
evaluation/test_prompts.json
```

The prompts vary across:

- **Themes:** Forest, Desert, Medieval City, Dungeon, Castle  
- **Difficulty levels:** 1–10  
- **Tone:** heroic, dark, mysterious, humorous, epic, serious  
- **Special constraints:** betrayal twist, political intrigue, espionage, rescue mission, forbidden magic  

---

# Automatic Evaluation

Lexical diversity is measured using:

- **Distinct-1** — ratio of unique unigrams  
- **Distinct-2** — ratio of unique bigrams  

Implemented in:

```
evaluation/eval_metrics.py
```

## Automatic Results (v2)

| Model      | Distinct-1 | Distinct-2 |
|------------|------------|------------|
| Baseline   | 0.355      | 0.889      |
| Finetuned  | 0.256      | 0.825      |

Although the baseline model achieved higher lexical diversity, this did not correspond to stronger narrative quality.
Automatic metrics alone were insufficient to capture semantic alignment and narrative control, reinforcing the importance of structured human evaluation.
---

# Human Evaluation

All 50 prompts were manually evaluated (100 generations total).

## Scoring Scale

- **1 = Poor**
- **2 = Partially satisfactory**
- **3 = Strong**

## Evaluation Criteria

### Coherence
- Logical narrative structure  
- Clear progression of events  
- Grammatical stability  

### Faithfulness
- Adherence to:
  - Level specification  
  - Setting  
  - Tone  
  - Additional constraints  

### Creativity
- Originality  
- Imaginative world-building  
- Narrative engagement  

Scores stored in:

```
evaluation/scores.csv
```

---

# Human Evaluation Results (v2)

| Model      | Coherence | Faithfulness | Creativity | Overall |
|------------|------------|--------------|------------|----------|
| Baseline   | 2.30       | 1.40         | 2.00       | 1.90     |
| Finetuned  | 2.84       | 1.86         | 2.76       | 2.49     |

---

# Key Findings

- Fine-tuning improved performance across all human metrics.
- Creativity showed the largest improvement (+0.76).
- Faithfulness improved significantly (+0.46).
- Coherence improved (+0.54).
- Overall mean score increased from **1.90 to 2.49**.

Fine-tuning enhances semantic control and narrative quality, even when lexical diversity slightly decreases.

---

# Reproducibility

1. Generate baseline and fine-tuned outputs.
2. Run:

```
python evaluation/eval_metrics.py
```

3. Score outputs using the rubric.
4. Compute averages from `scores.csv`.

All evaluation artifacts are located in:

```
evaluation/
```

---

# Team Documentation

- GitHub board: `docs/github_board.md`  
- Roles and tasks: `docs/team_roles.md`  

---

# Conclusion

QuestCrafter demonstrates that fine-tuning a compact language model on curated fantasy quest data significantly improves narrative coherence, creativity, and instruction adherence compared to a baseline model.
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

- **Gemima ONDELE POUROU** — data lead (`feat/data-pipeline`)
- **Fatima KACHALLAH** — evaluation lead (`feat/evaluation`)
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

### `feat/data_pipeline` — **Gemima ONDELE POUROU**

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
- Failure modes: `docs/failure_modes.md`
- Outputs: `outputs/baseline_generations.jsonl`,
  `outputs/finetuned_generations.jsonl`

#### Fine-tuned model (HF)

- **Model:** [Mr-MB/questcrafter-finetuned](https://huggingface.co/Mr-MB/questcrafter-finetuned)
- **Base:** distilgpt2 — 3 epochs on TinyStories (386 samples)

---

### `feat/evaluation` — **Fatima KACHALLAH**

#### Goal (Evaluation)

Compare baseline vs fine‑tuned generations using automatic metrics and a
human‑scored rubric on a fixed prompt set.

#### Artifacts (Evaluation)

- Prompt set: `evaluation/test_prompts.jsonl` (50 fixed prompts)
- Auto metrics: `evaluation/eval_metrics.py`
- Human scores: `evaluation/scores.csv`
- Generations: `evaluation/baseline_generations_v2.jsonl`,
  `evaluation/finetuned_generations_v2.jsonl`
- Full report: `README_EvaluationBranch_Final.md`

#### Results snapshot (v2)

| Model | Distinct-1 | Distinct-2 | Overall (Human) |
| --- | --- | --- | --- |
| Baseline | 0.355 | 0.889 | 1.90 |
| Finetuned | 0.256 | 0.825 | 2.49 |

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

### Fine-tuned model usage (HF)

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained("Mr-MB/questcrafter-finetuned")
tokenizer = GPT2Tokenizer.from_pretrained("Mr-MB/questcrafter-finetuned")
```

### Evaluation outputs (W2–W3)

Generated using the fixed prompt set (`evaluation/test_prompts.jsonl` on the
evaluation branch, 50 prompts):

- `outputs/baseline_generations.jsonl` — distilgpt2 baseline (50 outputs)
- `outputs/finetuned_generations.jsonl` — fine‑tuned model (50 outputs)

---

## ✅ Evaluation (W4)

Automatic metrics:
`python evaluation/eval_metrics.py`

Compare baseline vs tuned:
`python scripts/compare_outputs.py --baseline evaluation/baseline_generations_v2.jsonl --tuned evaluation/finetuned_generations_v2.jsonl --output outputs/compare_outputs.csv --top_n 20`

Human rubric:

- Template: `docs/human_rubric.md`
- CSV: `docs/human_eval_template.csv`
- Notebook: `notebooks/human_eval.ipynb`
 - Scores: `evaluation/scores.csv`

**Important:** human evaluation needs **lots of data**.  
Aim for **dozens to hundreds of scored rows**, ideally with multiple evaluators.

Quick example (CSV row):
`"prompt","baseline","tuned",3,4,3,4,"notes","evaluator","2026-02-06"`

---

## 📚 Team Docs

- GitHub board and issues: `docs/github_board.md`
- Roles, branches, and tasks: `docs/team_roles.md`
- Sample outputs: `docs/sample_outputs.md`
- Failure modes: `docs/failure_modes.md`
- Project brief: `docs/source_project_brief.pdf`
- Day 1 summary: `docs/source_day1_summary.pdf`

---

## 🛠️ Setup

- Python 3.10+
- `pip install -r requirements.txt`
