"""
Evaluation Methodology

We evaluate generated quests using both automatic and human-based metrics.
Automatic evaluation includes Distinct-1 and Distinct-2, which measure lexical
diversity by computing the ratio of unique unigrams and bigrams to the total
number of generated tokens. These metrics help identify repetitive or generic
outputs.

Human evaluation complements automatic metrics by scoring coherence,
prompt-faithfulness, and creativity on a 1–5 scale using a fixed rubric.
The same set of test prompts is used for all models to ensure fair and
reproducible comparison.
"""

import json
from collections import Counter

def load_generations(path):
    texts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["generation"])
    return texts

def distinct_n(texts, n=1):
    total_ngrams = 0
    unique_ngrams = set()

    for text in texts:
        tokens = text.split()
        ngrams = zip(*[tokens[i:] for i in range(n)])
        ngrams = list(ngrams)

        total_ngrams += len(ngrams)
        unique_ngrams.update(ngrams)

    if total_ngrams == 0:
        return 0.0

    return len(unique_ngrams) / total_ngrams

if __name__ == "__main__":
    baseline_texts = load_generations("evaluation/baseline_generations.jsonl")
    finetuned_texts = load_generations("evaluation/finetuned_generations.jsonl")

    print("Baseline Distinct-1:", distinct_n(baseline_texts, n=1))
    print("Baseline Distinct-2:", distinct_n(baseline_texts, n=2))

    print("Finetuned Distinct-1:", distinct_n(finetuned_texts, n=1))
    print("Finetuned Distinct-2:", distinct_n(finetuned_texts, n=2))
