---
slug: fine-tuning-lora
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Parameter-efficient fine-tuning of LLMs using LoRA (Low-Rank Adaptation) and its variants (QLoRA, DoRA, rsLoRA).
content_id: "4d13fa1c6ea48100"
tags: [lora, qlora, fine-tuning, adapters, llm]
---
# Fine-tuning (LoRA)

## Summary

**One-sentence:** Parameter-efficient fine-tuning of LLMs using LoRA (Low-Rank Adaptation) and its variants (QLoRA, DoRA, rsLoRA).

**One-paragraph:** Parameter-efficient fine-tuning of LLMs using LoRA (Low-Rank Adaptation) and its variants (QLoRA, DoRA, rsLoRA). LoRA trains small adapter layers (rank r) instead of updating all weights, reducing memory 10-20x while retaining 90-95% of full fine-tuning quality. Target all linear layers (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj), start with r=16, alpha=32, and mix 20-30% general data to prevent catastrophic forgetting.

## Applies If (ALL must hold)

- Need consistent domain-specific terminology or jargon the base model handles inconsistently
- Output format must be exact and reliable (JSON schema, medical codes, proprietary syntax)
- Inference cost reduction: fine-tuned models need shorter system prompts
- You have 500+ quality labeled examples in the target distribution
- Style/brand voice consistency required at high volume

## Skip If (ANY kills it)

- Fewer than 100 quality examples — few-shot prompting will outperform
- Requirements are changing — fine-tuned model becomes a liability when task evolves
- Need real-time knowledge — fine-tuning bakes in a snapshot; use RAG for live data
- No GPU access and limited budget — OpenAI fine-tuning API is a better path
- Model must handle wildly different tasks — specialized adapter degrades generality

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
