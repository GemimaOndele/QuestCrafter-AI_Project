import argparse
import random
from pathlib import Path

from jsonl_utils import load_jsonl, write_jsonl


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
