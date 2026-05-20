---
slug: fine-tuning-openai-production
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full OpenAI fine-tuning production pipeline: file upload, job creation with hyperparameter control, status polling, LLM-as-judge evaluation against a held-out test set, and model ID registry management.
content_id: "641e0ba788c8435c"
tags: [openai, fine-tuning, production, model-registry, evaluation]
---
# Fine-tuning OpenAI — Production

## Summary

**One-sentence:** Full OpenAI fine-tuning production pipeline: file upload, job creation with hyperparameter control, status polling, LLM-as-judge evaluation against a held-out test set, and model ID registry management.

**One-paragraph:** Full OpenAI fine-tuning production pipeline: file upload, job creation with hyperparameter control, status polling, LLM-as-judge evaluation against a held-out test set, and model ID registry management. The FineTuningPipeline class encapsulates the complete workflow with human-checkpoint gates before deployment.

## Applies If (ALL must hold)

- Need a fine-tuned model deployable via OpenAI API with zero infrastructure overhead
- Task has 50-10,000 high-quality JSONL examples with a consistent system prompt
- Use cases: style consistency, domain-specific tone, structured output format enforcement, task classifier
- Willing to tolerate 15 minutes to several hours of training latency

## Skip If (ANY kills it)

- Fewer than 50 examples — base model with few-shot beats fine-tuning; collect more data first
- Task requires up-to-date factual knowledge — OpenAI fine-tuning does not inject new facts
- Cost sensitivity: ft:gpt-4o-mini costs 3-6x more per token than base gpt-4o-mini — verify ROI
- Proprietary data that must not leave your infrastructure — training data is processed on OpenAI servers
- Need for a fully private model weight — OpenAI retains training data per their data policy

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

- parent skill: `geek/ai/ml-ops/`
