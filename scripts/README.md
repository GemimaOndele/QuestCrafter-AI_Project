# Scripts folder

Utility scripts used across the project.

Data pipeline:

- `download_data.py` (in repo root): download and split TinyStories
- `prepare_training_data.py`: convert JSONL splits to training-ready `text` field
- `compute_dataset_stats.py`: compute train/val/test token stats
- `make_sample_csv.py`: create small CSV samples for GitHub commits

Evaluation:

- `generate_outputs.py`: generate baseline/tuned outputs
- `evaluate_outputs.py`: compute simple lexical metrics
- `compare_outputs.py`: compare baseline vs tuned by length delta
- `build_human_eval_sheet.py`: build CSV sheet for human rubric scoring
- `make_eval_outputs.py`: export baseline/tuned JSONL from real responses

Repo hygiene:

- `check_large_files.py`: detect large files before commit
