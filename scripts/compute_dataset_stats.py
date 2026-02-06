import argparse
import json
from pathlib import Path


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def tokenize(text: str):
    return [t for t in text.split() if t]


def compute_stats(path: Path, field: str):
    lengths = []
    for record in load_jsonl(path):
        value = record.get(field, "")
        if not isinstance(value, str):
            continue
        tokens = tokenize(value)
        lengths.append(len(tokens))

    if not lengths:
        return {"count": 0, "avg": 0, "min": 0, "max": 0}

    return {
        "count": len(lengths),
        "avg": round(sum(lengths) / len(lengths), 2),
        "min": min(lengths),
        "max": max(lengths),
    }


def build_summary(stats, min_target, max_target):
    all_mins = [v["min"] for v in stats.values() if v["count"] > 0]
    all_maxs = [v["max"] for v in stats.values() if v["count"] > 0]
    if not all_mins or not all_maxs:
        return "No valid records found in splits."

    min_len = min(all_mins)
    max_len = max(all_maxs)
    if min_len >= min_target and max_len <= max_target:
        return (
            "The current splits contain medium-length stories with a tight length "
            "range. All splits sit comfortably inside the target band "
            f"({min_target}-{max_target} tokens), which supports the chosen QA "
            "thresholds and minimizes length outliers."
        )

    return (
        "The current splits contain medium-length stories with a wide length range. "
        f"Some records fall outside the target band ({min_target}-{max_target} "
        "tokens), which supports the need for length filtering in QA."
    )


def write_markdown(output_path: Path, stats, field, min_target, max_target):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "## Dataset stats (W1)",
        "",
        "These statistics are computed from the current JSONL splits in",
        "`data/raw/tinystories`. Token counts are simple whitespace splits on the",
        f"`{field}` field.",
        "",
        "### Current splits",
        "",
        "| Split | Samples | Avg tokens | Min tokens | Max tokens |",
        "| --- | --- | --- | --- | --- |",
    ]

    for split in ("train", "val", "test"):
        data = stats.get(split, {"count": 0, "avg": 0, "min": 0, "max": 0})
        name = "Validation" if split == "val" else split.capitalize()
        lines.append(
            f"| {name} | {data['count']} | {data['avg']:.2f} | {data['min']} | {data['max']} |"
        )

    lines.extend(
        [
            "",
            "### Short summary",
            "",
            build_summary(stats, min_target, max_target),
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Compute dataset stats for train/val/test splits."
    )
    parser.add_argument(
        "--input_dir",
        default="data/raw",
        help="Folder containing dataset splits (train/val/test.jsonl).",
    )
    parser.add_argument(
        "--dataset",
        default="tinystories",
        help="Dataset subfolder name under input_dir.",
    )
    parser.add_argument(
        "--field",
        default="response",
        help="Field to tokenize for stats.",
    )
    parser.add_argument(
        "--output",
        default="docs/dataset_stats.md",
        help="Markdown output path.",
    )
    parser.add_argument("--min_target", type=int, default=50)
    parser.add_argument("--max_target", type=int, default=300)
    args = parser.parse_args()

    input_root = Path(args.input_dir) / args.dataset
    splits = {
        "train": input_root / "train.jsonl",
        "val": input_root / "val.jsonl",
        "test": input_root / "test.jsonl",
    }

    for split, path in splits.items():
        if not path.exists():
            raise SystemExit(f"Missing split: {split} at {path}")

    stats = {split: compute_stats(path, args.field) for split, path in splits.items()}
    write_markdown(Path(args.output), stats, args.field, args.min_target, args.max_target)
    print(f"Wrote stats to {args.output}")


if __name__ == "__main__":
    main()
