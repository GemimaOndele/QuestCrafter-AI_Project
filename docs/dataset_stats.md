## Dataset stats (W1)

These statistics are computed from the current JSONL splits in
`data/raw/tinystories`. Token counts are simple whitespace splits on the
`response` field.

### Current splits

| Split | Samples | Avg tokens | Min tokens | Max tokens |
| --- | --- | --- | --- | --- |
| Train | 386 | 131.58 | 61 | 170 |
| Validation | 48 | 130.15 | 82 | 156 |
| Test | 49 | 131.90 | 79 | 157 |

### Short summary

The current splits contain medium-length stories with a tight length range. All splits sit comfortably inside the target band (50-300 tokens), which supports the chosen QA thresholds and minimizes length outliers.
