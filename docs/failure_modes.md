# Baseline Model Failure Modes — distilgpt2

**Author:** Mike-Brady (Modeling Lead)  
**Week:** W2  
**Model:** distilgpt2 (baseline, no fine-tuning)  
**Evaluated on:** 50 quest prompts from `evaluation/test_prompts.jsonl`

---

## Overview

After running baseline generation on all 50 fixed test prompts, several consistent
failure patterns were observed in distilgpt2's outputs. These are documented here
to inform Fatima's evaluation rubric and scoring criteria.

---

## Failure Mode 1 — Prompt Blindness

**Description:** The model largely ignores the specific instructions in the prompt.
It does not follow the requested level, setting, tone, or quest structure.

**Example:**
- Prompt: `"Create a level-1 fantasy quest set in a forest with a heroic tone."`
- Generation: `"The forest is filled with colorful plants and animals. Each day, there is a big,"`

The model generates a generic nature description rather than a quest narrative.
There is no hero, no objective, no conflict — none of the expected quest elements.

**Impact on evaluation:** Faithfulness score will be very low for baseline outputs.

---

## Failure Mode 2 — Repetitive Loops

**Description:** The model frequently enters repetitive loops, repeating the same
phrase or sentence multiple times with minor variations.

**Example observed pattern:**

"Why is this coffee so bad?"
"Why is this coffee so bad?"
"Why is this coffee so bad?"


This is a known weakness of small autoregressive models like distilgpt2 when
no repetition penalty is applied.

**Impact on evaluation:** Coherence and fluency scores will be penalized heavily.

---

## Failure Mode 3 — Tone Mismatch

**Description:** The model cannot distinguish between requested tones (heroic,
dark, mysterious, humorous). All outputs share a similar neutral-to-childlike
register, regardless of the tone instruction.

**Root cause:** distilgpt2 was pre-trained on general web text and fine-tuned
on TinyStories (children's stories). It defaults to that register regardless of prompt.

**Impact on evaluation:** Tone adherence dimension will score near 0 for baseline.

---

## Failure Mode 4 — No Quest Structure

**Description:** None of the baseline outputs produced recognizable quest elements:
no objective, no antagonist, no reward, no progression. The model treats the
prompt as a story opening rather than a structured task description.

**Expected structure (not produced):**
- Quest title
- Objective / goal
- Obstacles or enemies
- Reward

**Impact on evaluation:** Creativity and structure scores will be low.

---

## Failure Mode 5 — Abrupt / Incomplete Generations

**Description:** Many outputs end mid-sentence or mid-thought within the
100-token generation window, without any narrative closure.

**Root cause:** 100 max_new_tokens is insufficient for full quest descriptions,
and distilgpt2 has no mechanism to produce complete units of meaning.

**Recommendation:** For the fine-tuned model, consider increasing `max_new_tokens`
to 150 - 200 and applying a repetition penalty (`repetition_penalty=1.3`).

---

## Summary Table

| Failure Mode         | Severity | Affects Rubric Dimension     |
|----------------------|----------|------------------------------|
| Prompt blindness     | High     | Faithfulness                 |
| Repetitive loops     | High     | Coherence, Fluency           |
| Tone mismatch        | High     | Tone adherence               |
| No quest structure   | High     | Creativity, Structure        |
| Abrupt endings       | Medium   | Fluency, Completeness        |

---

## Conclusion

The baseline distilgpt2 model is not capable of following structured creative
instructions without fine-tuning. These failure modes serve as the lower-bound
benchmark against which the fine-tuned QuestCrafter model will be compared in W4.
