---
slug: fine-tuning-openai-dpo
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Direct Preference Optimization (DPO) trains OpenAI models on preference pairs — a preferred response and a non-preferred response for the same input — to align model behavior to subjective criteria like tone, style, safety, or brand voice.
content_id: "4ef61fd3bfd0ade4"
tags: [fine-tuning, openai, dpo, alignment, preference-optimization]
---
# OpenAI Direct Preference Optimization (DPO)

## Summary

**One-sentence:** Direct Preference Optimization (DPO) trains OpenAI models on preference pairs — a preferred response and a non-preferred response for the same input — to align model behavior to subjective criteria like tone, style, safety, or brand voice.

**One-paragraph:** Direct Preference Optimization (DPO) trains OpenAI models on preference pairs — a preferred response and a non-preferred response for the same input — to align model behavior to subjective criteria like tone, style, safety, or brand voice. DPO is applied after SFT when the optimization target is subjective rather than a clear correct answer.

## Applies If (ALL must hold)

- Subjective preferences: tone, formality, brand voice, response style — where no single output is "correct".
- Safety refinements: teach the model to prefer cautious, policy-compliant responses over direct but unsafe ones.
- After SFT: DPO is most effective when applied on top of an already SFT-tuned model, not from base.
- Output quality improvement when human raters reliably prefer one response over another.

## Skip If (ANY kills it)

- Clear correct answers exist — use SFT instead; DPO is for subjective alignment, not factual accuracy.
- Fewer than 50 quality preference pairs — generating good non-preferred responses is labor-intensive and DPO degrades with noisy pairs.
- Models other than gpt-4.1/gpt-4.1-mini/gpt-4.1-nano — DPO is not supported on gpt-4o family.
- Starting from a base model without SFT — DPO on base models produces unstable results; always SFT first.

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
