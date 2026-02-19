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
            data.append(json.loads(line.strip()))
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data', type=str, default='data/raw/tinystories/train.jsonl')
    parser.add_argument('--val_data',   type=str, default='data/raw/tinystories/val.jsonl')
    parser.add_argument('--output_dir', type=str, default='models/questcrafter-finetuned')
    parser.add_argument('--model',      type=str, default='distilgpt2')
    parser.add_argument('--epochs',     type=int, default=3)
    parser.add_argument('--batch_size', type=int, default=8)
    parser.add_argument('--max_samples',type=int, default=None)
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

    if args.max_samples:
        train_raw = train_raw[:args.max_samples]
        val_raw   = val_raw[:max(1, args.max_samples // 8)]

    print(f"   Train: {len(train_raw)} | Val: {len(val_raw)} samples")

    # Build text list
    train_texts = [d.get('prompt','') + ' ' + d.get('response','') for d in train_raw]
    val_texts   = [d.get('prompt','') + ' ' + d.get('response','') for d in val_raw]

    print("🔧 Tokenizing...")
    # Batch tokenize - much faster
    train_enc = tokenizer(train_texts, truncation=True, max_length=256, padding='max_length')
    val_enc   = tokenizer(val_texts,   truncation=True, max_length=256, padding='max_length')

    train_enc['labels'] = train_enc['input_ids'].copy()
    val_enc['labels']   = val_enc['input_ids'].copy()

    train_dataset = Dataset.from_dict(train_enc)
    val_dataset   = Dataset.from_dict(val_enc)

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
        learning_rate=5e-5,
        warmup_steps=50,
        weight_decay=0.01,
        load_best_model_at_end=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )

    print("🚀 Starting fine-tuning...")
    trainer.train()

    print(f"💾 Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("✅ Training complete!")

if __name__ == '__main__':
    main()
