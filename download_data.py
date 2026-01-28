import argparse
from pathlib import Path

from datasets import load_dataset


DATASET_CONFIGS = {
    "writingprompts": {
        "hf_id": "writingprompts",
        "prompt_field": "prompt",
        "response_field": "story",
    },
    "tinystories": {
        "hf_id": "roneneldan/TinyStories",
        "prompt_field": None,
        "response_field": "text",
    },
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def make_splits(dataset, seed: int):
    if "train" in dataset and "validation" in dataset and "test" in dataset:
        return dataset["train"], dataset["validation"], dataset["test"]

    if "train" in dataset and "test" in dataset:
        split = dataset["train"].train_test_split(test_size=0.2, seed=seed)
        val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
        return split["train"], val_test["train"], val_test["test"]

    split = dataset.train_test_split(test_size=0.2, seed=seed)
    val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
    return split["train"], val_test["train"], val_test["test"]


def normalize_records(dataset, prompt_field, response_field, source_name):
    def _map(example):
        prompt = example[prompt_field] if prompt_field else ""
        response = example[response_field]
        return {
            "prompt": prompt.strip(),
            "response": response.strip(),
            "source": source_name,
        }

    return dataset.map(_map, remove_columns=dataset.column_names)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download datasets for QuestCrafter.")
    parser.add_argument(
        "--dataset",
        choices=DATASET_CONFIGS.keys(),
        default="writingprompts",
        help="Dataset source to download from Hugging Face.",
    )
    parser.add_argument(
        "--output_dir",
        default="data/raw",
        help="Directory to save JSONL splits.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splits.")
    args = parser.parse_args()

    config = DATASET_CONFIGS[args.dataset]
    dataset = load_dataset(config["hf_id"])

    train, val, test = make_splits(dataset, args.seed)
    train = normalize_records(train, config["prompt_field"], config["response_field"], args.dataset)
    val = normalize_records(val, config["prompt_field"], config["response_field"], args.dataset)
    test = normalize_records(test, config["prompt_field"], config["response_field"], args.dataset)

    output_dir = Path(args.output_dir) / args.dataset
    ensure_dir(output_dir)

    train.to_json(output_dir / "train.jsonl", orient="records", lines=True)
    val.to_json(output_dir / "val.jsonl", orient="records", lines=True)
    test.to_json(output_dir / "test.jsonl", orient="records", lines=True)

    print(f"Saved splits to {output_dir}")


if __name__ == "__main__":
    main()
