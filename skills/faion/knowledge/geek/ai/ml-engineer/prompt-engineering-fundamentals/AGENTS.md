---
slug: prompt-engineering-fundamentals
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prompt engineering is the practice of crafting inputs to LLMs that reliably produce desired outputs.
content_id: "4fafe581bfedfe3c"
tags: [prompt-engineering, few-shot, zero-shot, llm, system-prompt]
---
# Prompt Engineering Fundamentals

## Summary

**One-sentence:** Prompt engineering is the practice of crafting inputs to LLMs that reliably produce desired outputs.

**One-paragraph:** Prompt engineering is the practice of crafting inputs to LLMs that reliably produce desired outputs. It encompasses instruction design, context management, output control, and iterative evaluation. This methodology covers the foundational building blocks every practitioner needs before moving to advanced techniques.

## Applies If (ALL must hold)

- Inconsistent outputs from an LLM — structured prompts reduce variance.
- Wrong or unpredictable output format — output specifications guide the model.
- Missing context causing poor accuracy — background info section fixes this.
- Complex reasoning tasks that need step-by-step guidance.
- Any production system where tested, versioned prompts reduce failures.

## Skip If (ANY kills it)

- Model lacks the capability — prompt engineering cannot compensate; fine-tune or switch models.
- Task requires real-time data — use RAG with retrieval instead.
- Domain-specific knowledge is the gap — fine-tune with domain data.
- Consistent structured output is the sole goal — use the API's structured output / JSON schema mode.
- Complex multi-step workflows — use an agent framework (LangChain, etc.).
- Cost is the primary constraint — smaller model plus fine-tuning beats prompt overhead.

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
