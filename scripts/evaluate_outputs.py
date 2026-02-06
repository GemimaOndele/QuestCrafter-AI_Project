import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def pick_response_field(record):
    for key in ("response", "output", "text"):
        if key in record and isinstance(record[key], str):
            return key
    return None


def tokenize(text: str):
    return [t for t in text.strip().split() if t]


def distinct_n(tokens, n):
    if len(tokens) < n or n <= 0:
        return 0.0
    ngrams = [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
    return len(set(ngrams)) / max(1, len(ngrams))


def compute_metrics(records, min_chars):
    responses = []
    for record in records:
        key = pick_response_field(record)
        if not key:
            continue
        text = record[key].strip()
        if len(text) < min_chars:
            continue
        responses.append(text)

    if not responses:
        return {
            "count": 0,
            "avg_chars": 0,
            "avg_tokens": 0,
            "distinct_1": 0,
            "distinct_2": 0,
        }

    token_lists = [tokenize(text) for text in responses]
    all_tokens = [t for tokens in token_lists for t in tokens]

    avg_chars = sum(len(t) for t in responses) / len(responses)
    avg_tokens = sum(len(t) for t in token_lists) / len(token_lists)
    return {
        "count": len(responses),
        "avg_chars": round(avg_chars, 2),
        "avg_tokens": round(avg_tokens, 2),
        "distinct_1": round(distinct_n(all_tokens, 1), 4),
        "distinct_2": round(distinct_n(all_tokens, 2), 4),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute simple lexical metrics for generated outputs."
    )
    parser.add_argument("--baseline", required=True, help="Path to baseline JSONL.")
    parser.add_argument("--tuned", default=None, help="Path to tuned JSONL.")
    parser.add_argument(
        "--min_chars",
        type=int,
        default=20,
        help="Minimum response length to include.",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Optional path to write JSON report.",
    )
    args = parser.parse_args()

    baseline_records = list(load_jsonl(Path(args.baseline)))
    report = {"baseline": compute_metrics(baseline_records, args.min_chars)}

    if args.tuned:
        tuned_records = list(load_jsonl(Path(args.tuned)))
        report["tuned"] = compute_metrics(tuned_records, args.min_chars)

    print(json.dumps(report, indent=2))
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.report).open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)


if __name__ == "__main__":
    main()
