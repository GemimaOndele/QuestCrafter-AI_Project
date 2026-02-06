## Roles, branches, and tasks (entire project)

### Team
- Gemima Ondele
- Kachallah Fatima
- Mike-Brady
- Joseph Fabrice TSAPFACK

### Branch assignment (primary)
- Gemima: `feat/data-pipeline` (data lead)
- Fatima: `feat/evaluation` (evaluation lead)
- Mike: `feat/training` (modeling lead)
- Joseph: `feat/demo` (demo and packaging lead)

### Roles and tasks by week

W1 (Dataset pipeline)
- Gemima (data lead)
  - Implement `download_data.py` cleaning + filters
  - Export JSONL splits
  - Validate schema consistency
- Fatima (data QA + docs)
  - Define filtering thresholds
  - Produce dataset stats and short summary
  - Update README pipeline section
- Mike (data QA)
  - Verify split ratios and random seed
  - Smoke test JSONL loading
- Joseph (repo hygiene)
  - Maintain folder structure
  - Update `CONTRIBUTING.md` and doc links

W2 (Baseline + rubric)
- Gemima
  - Baseline generation script setup
  - Save sample outputs for review
- Fatima (evaluation lead)
  - Define test prompt set (50+)
  - Create human rubric (coherence, creativity, faithfulness)
- Mike
  - Configure baseline model settings (distilgpt2)
  - Document failure modes
- Joseph
  - Organize evaluation artifacts in repo

W3 (Fine-tuning)
- Gemima
  - Data loader and training-ready format check
- Mike (modeling lead)
  - Fine-tuning script (HF Trainer)
  - Track training curves and checkpoints
- Fatima
  - Prepare evaluation notebook/script for W4
- Joseph
  - Ensure reproducible run steps in README

W4 (Control + evaluation)
- Gemima
  - Add control fields (level/setting/tone) in prompts if used
- Fatima (evaluation lead)
  - Run baseline vs tuned evaluation
  - Summarize metrics and rubric scores
- Mike
  - Assist with controllability tests
- Joseph
  - Compile examples for report/presentation

W5 (Demo + report)
- Gemima
  - Final polish on data/scripts
- Fatima
  - Lead report writing (4-8 pages)
- Mike
  - Final model selection and results tables
- Joseph (demo lead)
  - Build Streamlit/Gradio demo
  - Prepare presentation slides
