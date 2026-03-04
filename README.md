# QuestCrafter-AI_Project

QuestCrafter is a lightweight generative AI system designed to function as a miniature “Dungeon Master” for RPG-style quest generation. The project fine-tunes a small language model on curated fantasy prompt-to-quest data derived from the TinyStories dataset, compares baseline and fine-tuned outputs, evaluates generation quality using both automatic and human metrics, and provides an interactive demo interface.

---

## Setup

### Requirements
- Python 3.10+
- Virtual environment recommended

Branch report: feat/evaluation
Owner: Fatima KACHALLAH


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
