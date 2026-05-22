---
slug: finetuning
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A general guide to fine-tuning LLMs covering the decision framework (prompt → RAG → fine-tune), technique selection (Full FT, LoRA, QLoRA, DoRA, OpenAI API), and framework comparison (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune).
content_id: "d0da5f1ecc62094d"
tags: [fine-tuning, decision-tree, frameworks, llm, data-pipeline]
---
# LLM Fine-tuning (General Guide)

## Summary

**One-sentence:** A general guide to fine-tuning LLMs covering the decision framework (prompt → RAG → fine-tune), technique selection (Full FT, LoRA, QLoRA, DoRA, OpenAI API), and framework comparison (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune).

**One-paragraph:** A general guide to fine-tuning LLMs covering the decision framework (prompt → RAG → fine-tune), technique selection (Full FT, LoRA, QLoRA, DoRA, OpenAI API), and framework comparison (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune). Always follow the decision tree before committing to fine-tuning — it is the most expensive and least reversible enhancement strategy.

## Applies If (ALL must hold)

- Prompt engineering and RAG have both been tried and still fail to meet quality bar
- Domain jargon, output format, or behavioral style needs to be internalized rather than injected per-call
- Production volume is high enough that shorter prompts reduce inference cost meaningfully
- You have 500+ verified examples in the target distribution with clear correct/incorrect labels
- Compliance requires a local or private model with no external API calls

## Skip If (ANY kills it)

- Fewer than 100 quality examples — fine-tuning will overfit; use few-shot prompting
- Task requirements are exploratory or changing — fine-tuning creates a liability that degrades as the task evolves
- Real-time knowledge is required — use RAG for dynamic data
- Time-to-production is critical — fine-tuning adds days of iteration; try prompting first
- No labeled data exists — data collection must precede training

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
