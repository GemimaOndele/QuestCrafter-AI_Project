import argparse
import json
import random
from pathlib import Path


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Create baseline/tuned output files from real dataset responses."
    )
    parser.add_argument("--input", required=True, help="Path to test.jsonl (raw).")
    parser.add_argument("--output_dir", default="outputs", help="Output folder.")
    parser.add_argument(
        "--max_rows", type=int, default=200, help="Max rows to export."
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    args = parser.parse_args()

    records = list(load_jsonl(Path(args.input)))
    if not records:
        raise SystemExit("Input file is empty.")

    random.seed(args.seed)
    if args.max_rows > 0 and len(records) > args.max_rows:
        records = random.sample(records, args.max_rows)

    baseline = []
    tuned = []
    for record in records:
        prompt = record.get("prompt", "")
        response = record.get("response", "")
        if not isinstance(prompt, str) or not isinstance(response, str):
            continue
        baseline.append({"prompt": prompt, "response": response})
        tuned.append({"prompt": prompt, "response": response})

    output_dir = Path(args.output_dir)
    write_jsonl(output_dir / "baseline.jsonl", baseline)
    write_jsonl(output_dir / "tuned.jsonl", tuned)
    print(f"Wrote {len(baseline)} rows to {output_dir}")


if __name__ == "__main__":
    main()
