import json
import argparse
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_test_data(input_path):
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def generate_text(model, tokenizer, prompt, max_new_tokens=100, temperature=0.7, top_p=0.9, device='cpu'):
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text[len(prompt):].strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/raw/tinystories/test.jsonl')
    parser.add_argument('--output', type=str, default='outputs/baseline.jsonl')
    parser.add_argument('--model', type=str, default='distilgpt2')
    parser.add_argument('--max_samples', type=int, default=None)
    parser.add_argument('--max_new_tokens', type=int, default=100)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Using device: {device}")

    print(f"🤖 Loading model: {args.model}")
    tokenizer = GPT2Tokenizer.from_pretrained(args.model)
    model = GPT2LMHeadModel.from_pretrained(args.model)
    model.to(device)
    model.eval()

    print(f"📖 Loading test data from: {args.input}")
    test_data = load_test_data(args.input)

    if args.max_samples:
        test_data = test_data[:args.max_samples]
        print(f"⚠️  Processing only {args.max_samples} samples (testing mode)")

    print(f"📝 Generating outputs for {len(test_data)} samples...")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = []
    for item in tqdm(test_data, desc="Generating"):
        prompt = item.get('prompt', '')
        if not prompt:
            prompt = item.get('response', '')[:50]

        generation = generate_text(
            model, tokenizer, prompt,
            max_new_tokens=args.max_new_tokens,
            device=device
        )

        results.append({
            'prompt': prompt,
            'generation': generation
        })

    print(f"💾 Saving results to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    print(f"✅ Done! Generated {len(results)} outputs")
    print(f"📊 Sample:")
    print(f"   Prompt: {results[0]['prompt'][:80]}")
    print(f"   Generation: {results[0]['generation'][:80]}")

if __name__ == '__main__':
    main()
