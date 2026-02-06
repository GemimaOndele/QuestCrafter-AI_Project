import argparse
import csv
from pathlib import Path

from jsonl_utils import load_jsonl


def main():
    parser = argparse.ArgumentParser(
        description="Compare baseline vs tuned outputs and export a CSV."
    )
    parser.add_argument("--baseline", required=True, help="Path to baseline JSONL.")
    parser.add_argument("--tuned", required=True, help="Path to tuned JSONL.")
    parser.add_argument(
        "--output",
        default="outputs/compare_outputs.csv",
        help="Path to output CSV.",
    )
    parser.add_argument("--top_n", type=int, default=20, help="Rows to export.")
    args = parser.parse_args()

    baseline = list(load_jsonl(Path(args.baseline)))
    tuned = list(load_jsonl(Path(args.tuned)))

    tuned_by_prompt = {r.get("prompt", ""): r.get("response", "") for r in tuned}
    rows = []
    for record in baseline:
        prompt = record.get("prompt", "")
        base = record.get("response", "")
        tune = tuned_by_prompt.get(prompt, "")
        if not isinstance(base, str) or not isinstance(tune, str):
            continue
        rows.append(
            {
                "prompt": prompt,
                "baseline_response": base,
                "tuned_response": tune,
                "baseline_len": len(base),
                "tuned_len": len(tune),
                "delta_len": len(tune) - len(base),
            }
        )

    rows.sort(key=lambda r: abs(r["delta_len"]), reverse=True)
    if args.top_n > 0:
        rows = rows[: args.top_n]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "prompt",
                "baseline_response",
                "tuned_response",
                "baseline_len",
                "tuned_len",
                "delta_len",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
