import argparse
import csv
from pathlib import Path

from jsonl_utils import load_jsonl


def main():
    parser = argparse.ArgumentParser(
        description="Build a CSV sheet for human rubric evaluation."
    )
    parser.add_argument("--baseline", required=True, help="Path to baseline JSONL.")
    parser.add_argument("--tuned", required=True, help="Path to tuned JSONL.")
    parser.add_argument(
        "--output",
        default="docs/human_eval_template.csv",
        help="Path to output CSV.",
    )
    args = parser.parse_args()

    baseline_records = list(load_jsonl(Path(args.baseline)))
    tuned_records = list(load_jsonl(Path(args.tuned)))

    tuned_by_prompt = {r.get("prompt", ""): r.get("response", "") for r in tuned_records}

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "prompt",
        "baseline_response",
        "tuned_response",
        "coherence_1_5",
        "creativity_1_5",
        "faithfulness_1_5",
        "overall_1_5",
        "notes",
        "evaluator",
        "date",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in baseline_records:
            prompt = record.get("prompt", "")
            baseline = record.get("response", "")
            tuned = tuned_by_prompt.get(prompt, "")
            writer.writerow(
                {
                    "prompt": prompt,
                    "baseline_response": baseline,
                    "tuned_response": tuned,
                    "coherence_1_5": "",
                    "creativity_1_5": "",
                    "faithfulness_1_5": "",
                    "overall_1_5": "",
                    "notes": "",
                    "evaluator": "",
                    "date": "",
                }
            )

    print(f"Wrote template to {output_path}")


if __name__ == "__main__":
    main()
