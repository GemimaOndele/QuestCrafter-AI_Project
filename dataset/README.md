# Dataset folder

This folder stores small, tracked dataset artifacts used for documentation.
Large raw datasets are ignored by git and should live in `data/raw/`.

Contents:

- `sample/`: small CSV samples for GitHub
- `tinystories-narrative-classification-metadata.json`: TinyStories metadata

To regenerate samples:
`python scripts/make_sample_csv.py --input_dir dataset --output_dir dataset/sample --max_rows 1000`
