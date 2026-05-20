---
slug: fine-tuning-openai-eval
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Before routing production traffic to a fine-tuned model, evaluate it against the base model on a held-out test set using automated LLM-as-judge scoring and A/B comparison.
content_id: "3c89f9843c0a25b5"
tags: [fine-tuning, openai, evaluation, llm-as-judge, model-comparison]
---
# OpenAI Fine-Tuning Evaluation

## Summary

**One-sentence:** Before routing production traffic to a fine-tuned model, evaluate it against the base model on a held-out test set using automated LLM-as-judge scoring and A/B comparison.

**One-paragraph:** Before routing production traffic to a fine-tuned model, evaluate it against the base model on a held-out test set using automated LLM-as-judge scoring and A/B comparison. Eval must pass quality gates on accuracy, format compliance, and human preference rate before deployment is approved.

## Applies If (ALL must hold)

- After every fine-tuning job completes, before any production traffic is routed to the new model.
- When deciding whether to increase epoch count or add more training data.
- When comparing multiple fine-tuned model candidates (different hyperparameters, different data versions).
- Periodic regression testing after retraining on updated datasets.

## Skip If (ANY kills it)

- Evaluating base models without fine-tuning context — use standard benchmarks instead.
- Replacing human review entirely — automated eval catches metric regressions, not all failure modes.

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
