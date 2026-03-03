import json
import argparse
from pathlib import Path
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import torch

def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(json.loads(line))
    return data

# ✅ FIX 1: Filter out repetitive training samples
def calculate_repetition_ratio(text):
    tokens = text.split()
    if len(tokens) < 2:
        return 0
    bigrams = list(zip(tokens[:-1], tokens[1:]))
    return len(set(bigrams)) / len(bigrams)

def tokenize_data(examples, tokenizer, max_length=256):
    # ✅ FIX 2: Structured prompt conditioning
    texts = []
    for item in examples:
        prompt = item.get('prompt', '')
        response = item.get('response', '')
        # Add setting/level/tone tokens if available
        level   = item.get('level', '')
        setting = item.get('setting', '')
        tone    = item.get('tone', '')
        prefix = ''
        if level:   prefix += f'<LEVEL={level}>'
        if setting: prefix += f'<SETTING={setting}>'
        if tone:    prefix += f'<TONE={tone}>'
        texts.append(f"{prefix}{prompt} {response}")
    
    tokenized = tokenizer(
        texts,
        truncation=True,
        max_length=max_length,
        padding='max_length'
    )
    tokenized['labels'] = tokenized['input_ids'].copy()
    return tokenized

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data',  type=str, default='data/raw/tinystories/train.jsonl')
    parser.add_argument('--val_data',    type=str, default='data/raw/tinystories/val.jsonl')
    parser.add_argument('--output_dir',  type=str, default='models/questcrafter-finetuned')
    parser.add_argument('--model',       type=str, default='distilgpt2')
    parser.add_argument('--epochs',      type=int, default=5)       # ✅ FIX 3: More epochs
    parser.add_argument('--batch_size',  type=int, default=8)
    parser.add_argument('--max_samples', type=int, default=None)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Using device: {device}")
    print(f"🤖 Loading model: {args.model}")
    tokenizer = GPT2Tokenizer.from_pretrained(args.model)
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(args.model)

    print("📖 Loading data...")
    train_raw = load_jsonl(args.train_data)
    val_raw   = load_jsonl(args.val_data)

    # ✅ FIX 1: Filter repetitive samples from training set
    before = len(train_raw)
    train_raw = [d for d in train_raw if calculate_repetition_ratio(
        d.get('prompt','') + ' ' + d.get('response','')) > 0.4]
    print(f"🧹 Filtered: {before} → {len(train_raw)} training samples (removed repetitive ones)")

    if args.max_samples:
        train_raw = train_raw[:args.max_samples]
        val_raw   = val_raw[:max(1, args.max_samples // 8)]
    print(f"Train: {len(train_raw)} | Val: {len(val_raw)} samples")

    print("🔧 Tokenizing...")
    train_tok = tokenize_data(train_raw, tokenizer)
    val_tok   = tokenize_data(val_raw,   tokenizer)
    train_dataset = Dataset.from_dict(train_tok)
    val_dataset   = Dataset.from_dict(val_tok)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    print("✅ Tokenizing done!")

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        learning_rate=2e-5,          # ✅ FIX 4: Lower LR (was 5e-5)
        warmup_steps=100,            # ✅ FIX 5: More warmup (was 50)
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )

    print("🚀 Starting fine-tuning...")
    trainer.train()

    print(f"💾 Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("✅ Training complete!")

if __name__ == '__main__':
    main()
