import argparse
import json
from pathlib import Path

import datasets


def write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_control_prefix(record, control_keys, control_format, drop_missing):
    if not control_keys:
        return ""

    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    parts = []
    for key in control_keys:
        value = record.get(key, None)
        if value in (None, ""):
            value = metadata.get(key, None)
        if value in (None, ""):
            if drop_missing:
                return None
            continue
        parts.append(control_format.format(key=key, value=str(value)))
    return "".join(parts)


def to_training_record(record, args):
    prompt = record.get("prompt", "")
    response = record.get("response", "")
    if not isinstance(prompt, str) or not isinstance(response, str):
        return None

    control_prefix = build_control_prefix(
        record, args.control_keys, args.control_format, args.drop_missing_control
    )
    if control_prefix is None:
        return None

    text = f"{control_prefix}{args.prompt_prefix}{prompt}{args.separator}{args.response_prefix}{response}"

    out = dict(record)
    out["text"] = text
    return out


def process_split(path: Path, args):
    dataset = datasets.load_dataset("json", data_files=str(path), split="train")
    output = []
    dropped = 0
    for record in dataset:
        out = to_training_record(record, args)
        if out is None:
            dropped += 1
            continue
        output.append(out)
    return output, dropped


def main():
    parser = argparse.ArgumentParser(
        description="Prepare training-ready JSONL with a single 'text' field."
    )
    parser.add_argument(
        "--input_dir",
        default="data/raw",
        help="Folder containing dataset splits (train/val/test.jsonl).",
    )
    parser.add_argument(
        "--dataset",
        default="redditjokes",
        help="Dataset subfolder name under input_dir/output_dir.",
    )
    parser.add_argument(
        "--output_dir",
        default="data/processed",
        help="Folder to write processed splits.",
    )
    parser.add_argument(
        "--prompt_prefix",
        default="User: ",
        help="Prefix before the prompt.",
    )
    parser.add_argument(
        "--response_prefix",
        default="Assistant: ",
        help="Prefix before the response.",
    )
    parser.add_argument(
        "--separator",
        default="\n\n",
        help="Separator between prompt and response.",
    )
    parser.add_argument(
        "--control_keys",
        default="",
        help="Comma-separated control keys to prepend (e.g. level,setting,tone).",
    )
    parser.add_argument(
        "--control_format",
        default="[{key}:{value}] ",
        help="Format string for control tokens.",
    )
    parser.add_argument(
        "--drop_missing_control",
        action="store_true",
        help="Drop rows missing any requested control key.",
    )
    args = parser.parse_args()

    args.control_keys = [k.strip() for k in args.control_keys.split(",") if k.strip()]

    input_root = Path(args.input_dir) / args.dataset
    output_root = Path(args.output_dir) / args.dataset

    for split_name, out_name in (("train", "train"), ("val", "validation"), ("test", "test")):
        input_path = input_root / f"{split_name}.jsonl"
        if not input_path.exists():
            raise SystemExit(f"Missing split: {input_path}")

        records, dropped = process_split(input_path, args)
        output_path = output_root / f"{out_name}.jsonl"
        write_jsonl(output_path, records)
        print(f"{split_name}: {len(records)} rows (dropped {dropped}) -> {output_path}")


if __name__ == "__main__":
    main()
