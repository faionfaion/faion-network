---
slug: fine-tuning-openai-sft
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Supervised Fine-Tuning (SFT) customizes OpenAI GPT-4.
content_id: "c8b667f65ed324cb"
tags: [fine-tuning, openai, sft, gpt, training]
---
# OpenAI Supervised Fine-Tuning (SFT)

## Summary

**One-sentence:** Supervised Fine-Tuning (SFT) customizes OpenAI GPT-4.

**One-paragraph:** Supervised Fine-Tuning (SFT) customizes OpenAI GPT-4.1 and GPT-4o models by training on input-output pairs in JSONL format. It is the default and primary fine-tuning method: upload a JSONL training file, create a fine-tuning job, poll for completion, then use the returned model ID in production.

## Applies If (ALL must hold)

- Clear correct answers exist and 50+ high-quality labeled examples are available.
- Domain-specific tasks where the base model underperforms (medical coding, legal extraction, brand voice).
- Reducing long system prompts that are repeated on every call — internalize them into the model.
- Consistent structured output (JSON schema, specific formats) is required at high call volume.
- Prompt engineering alone cannot achieve the required quality bar.

## Skip If (ANY kills it)

- Fewer than 50 quality labeled examples — use few-shot prompting instead; SFT with noisy data degrades quality.
- Real-time data dependency — fine-tuned models have a static knowledge snapshot; use RAG.
- Need a private or on-premise model — OpenAI fine-tuned models stay on OpenAI infrastructure; weights are not exported.
- Task is exploratory or requirements change within weeks — retrain cost makes iteration prohibitive.
- Low call volume — inference cost premium over base model does not pay off.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
