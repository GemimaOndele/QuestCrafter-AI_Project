import argparse
import re
from pathlib import Path

import datasets


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
    "redditjokes": {
        "hf_id": None,
        "prompt_field": "title",
        "response_field": "body",
    },
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_columns(dataset):
    if isinstance(dataset, dict):
        for split in ("train", "validation", "test"):
            if split in dataset:
                return dataset[split].column_names
        first_split = next(iter(dataset.keys()))
        return dataset[first_split].column_names
    return dataset.column_names


def resolve_field(columns, field_name, fallbacks):
    if field_name and field_name in columns:
        return field_name
    for candidate in fallbacks:
        if candidate in columns:
            return candidate
    return None


def make_splits(dataset, seed: int):
    if isinstance(dataset, dict):
        if "train" in dataset and "validation" in dataset and "test" in dataset:
            return dataset["train"], dataset["validation"], dataset["test"]

        if "train" in dataset and "test" in dataset:
            split = dataset["train"].train_test_split(test_size=0.2, seed=seed)
            val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
            return split["train"], val_test["train"], val_test["test"]

        base_split = dataset.get("train") or dataset[next(iter(dataset.keys()))]
        split = base_split.train_test_split(test_size=0.2, seed=seed)
        val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
        return split["train"], val_test["train"], val_test["test"]

    if "train" in dataset and "validation" in dataset and "test" in dataset:
        return dataset["train"], dataset["validation"], dataset["test"]

    if "train" in dataset and "test" in dataset:
        split = dataset["train"].train_test_split(test_size=0.2, seed=seed)
        val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
        return split["train"], val_test["train"], val_test["test"]

    split = dataset.train_test_split(test_size=0.2, seed=seed)
    val_test = split["test"].train_test_split(test_size=0.5, seed=seed)
    return split["train"], val_test["train"], val_test["test"]


def clean_text(text):
    if text is None:
        return ""
    cleaned = str(text).replace("\r", " ").replace("\n", " ").strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def should_drop_deleted(text):
    lowered = text.strip().lower()
    return lowered in {"[deleted]", "[removed]"}


def normalize_records(dataset, prompt_field, response_field, source_name, include_metadata):
    def _map(example):
        prompt = clean_text(example[prompt_field]) if prompt_field else ""
        response = clean_text(example[response_field])

        record = {
            "prompt": prompt.strip(),
            "response": response.strip(),
            "source": source_name,
        }

        if include_metadata:
            metadata = {}
            for key in ("score", "author", "id", "subreddit"):
                if key in example and example[key] not in (None, ""):
                    metadata[key] = example[key]
            if metadata:
                record["metadata"] = metadata

        return record

    return dataset.map(_map, remove_columns=dataset.column_names)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download datasets for QuestCrafter.")
    parser.add_argument(
        "--dataset",
        choices=DATASET_CONFIGS.keys(),
        default="redditjokes",
        help="Dataset source to download from Hugging Face or local CSV.",
    )
    parser.add_argument(
        "--output_dir",
        default="data/raw",
        help="Directory to save JSONL splits.",
    )
    parser.add_argument(
        "--local_csv",
        default=None,
        help="Path to a local CSV file (required for redditjokes).",
    )
    parser.add_argument(
        "--prompt_field",
        default=None,
        help="Optional prompt column name override.",
    )
    parser.add_argument(
        "--response_field",
        default=None,
        help="Optional response column name override.",
    )
    parser.add_argument(
        "--min_prompt_chars",
        type=int,
        default=5,
        help="Minimum prompt length (characters). Ignored if prompt field is empty.",
    )
    parser.add_argument(
        "--max_prompt_chars",
        type=int,
        default=300,
        help="Maximum prompt length (characters). Ignored if prompt field is empty.",
    )
    parser.add_argument(
        "--min_response_chars",
        type=int,
        default=20,
        help="Minimum response length (characters).",
    )
    parser.add_argument(
        "--max_response_chars",
        type=int,
        default=800,
        help="Maximum response length (characters).",
    )
    parser.add_argument(
        "--keep_deleted",
        action="store_true",
        help="Keep rows with [deleted]/[removed] responses (default: drop).",
    )
    parser.add_argument(
        "--no_metadata",
        action="store_true",
        help="Disable metadata fields in JSONL output.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splits.")
    args = parser.parse_args()

    config = DATASET_CONFIGS[args.dataset]
    if config["hf_id"]:
        dataset = datasets.load_dataset(config["hf_id"])
    else:
        if not args.local_csv:
            raise ValueError("For redditjokes, you must provide --local_csv.")
        csv_path = Path(args.local_csv)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV not found: {csv_path}")
        dataset = datasets.load_dataset("csv", data_files=str(csv_path))

    columns = get_columns(dataset)
    prompt_field = resolve_field(
        columns,
        args.prompt_field or config["prompt_field"],
        ["prompt", "title", "question", "setup", "context"],
    )
    response_field = resolve_field(
        columns,
        args.response_field or config["response_field"],
        ["response", "body", "joke", "Joke", "text", "completion", "answer"],
    )
    if response_field is None:
        raise ValueError(f"Response column not found in CSV. Columns: {columns}")

    def is_valid(example):
        prompt = clean_text(example[prompt_field]) if prompt_field else ""
        response = clean_text(example[response_field])

        if not response:
            return False
        if not args.keep_deleted and should_drop_deleted(response):
            return False

        if prompt_field:
            if len(prompt) < args.min_prompt_chars:
                return False
            if len(prompt) > args.max_prompt_chars:
                return False

        if len(response) < args.min_response_chars:
            return False
        if len(response) > args.max_response_chars:
            return False

        return True

    dataset = dataset.filter(is_valid)

    train, val, test = make_splits(dataset, args.seed)
    include_metadata = not args.no_metadata
    train = normalize_records(train, prompt_field, response_field, args.dataset, include_metadata)
    val = normalize_records(val, prompt_field, response_field, args.dataset, include_metadata)
    test = normalize_records(test, prompt_field, response_field, args.dataset, include_metadata)

    output_dir = Path(args.output_dir) / args.dataset
    ensure_dir(output_dir)

    train.to_json(output_dir / "train.jsonl", orient="records", lines=True)
    val.to_json(output_dir / "val.jsonl", orient="records", lines=True)
    test.to_json(output_dir / "test.jsonl", orient="records", lines=True)

    print(f"Saved splits to {output_dir}")


if __name__ == "__main__":
    main()
