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


def write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate model outputs from prompts (baseline or tuned)."
    )
    parser.add_argument("--input", required=True, help="Path to test.jsonl (raw).")
    parser.add_argument("--output", required=True, help="Path to output JSONL.")
    parser.add_argument(
        "--model_id",
        default="distilgpt2",
        help="HF model id (baseline or fine-tuned).",
    )
    parser.add_argument(
        "--prompt_field",
        default="prompt",
        help="Field to read prompt from.",
    )
    parser.add_argument(
        "--fallback_field",
        default="response",
        help="Fallback field if prompt is empty (use '' to disable).",
    )
    parser.add_argument(
        "--max_rows", type=int, default=200, help="Max prompts to generate."
    )
    parser.add_argument(
        "--max_new_tokens", type=int, default=120, help="Max new tokens to generate."
    )
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        from transformers import pipeline, set_seed
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: transformers. Install with:\n"
            "pip install transformers torch"
        ) from exc

    records = list(load_jsonl(Path(args.input)))
    if not records:
        raise SystemExit("Input file is empty.")

    if args.max_rows > 0:
        records = records[: args.max_rows]

    set_seed(args.seed)
    generator = pipeline(
        "text-generation",
        model=args.model_id,
    )

    outputs = []
    for record in records:
        prompt = record.get(args.prompt_field, "")
        if not isinstance(prompt, str) or not prompt.strip():
            fallback = args.fallback_field or ""
            prompt = record.get(fallback, "") if fallback else ""
        if not isinstance(prompt, str) or not prompt.strip():
            continue
        result = generator(
            prompt,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            do_sample=True,
            num_return_sequences=1,
        )[0]["generated_text"]
        outputs.append({"prompt": prompt, "response": result})

    write_jsonl(Path(args.output), outputs)
    print(f"Wrote {len(outputs)} rows to {args.output}")


if __name__ == "__main__":
    main()
