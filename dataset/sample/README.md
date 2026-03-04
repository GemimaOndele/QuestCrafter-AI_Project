# Dataset samples

This folder contains small CSV samples for GitHub reviews.
It mirrors the main CSV files but with fewer rows.

Regenerate from the full dataset:
python scripts/make_sample_csv.py --input_dir dataset --output_dir dataset/sample --max_rows 1000

Notes:

- Keep samples small to avoid large commits.
- Files in this folder are safe to commit.
