---
slug: fine-tuning-openai-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Data preparation methodology for OpenAI fine-tuning: creating JSONL training examples in the chat messages format, validating structure and token counts with tiktoken, and generating additional examples with GPT-4.
content_id: "f5a3fb2047ff8e62"
tags: [openai, fine-tuning, data-preparation, validation, cost-estimation]
---
# Fine-tuning OpenAI — Basics

## Summary

**One-sentence:** Data preparation methodology for OpenAI fine-tuning: creating JSONL training examples in the chat messages format, validating structure and token counts with tiktoken, and generating additional examples with GPT-4.

**One-paragraph:** Data preparation methodology for OpenAI fine-tuning: creating JSONL training examples in the chat messages format, validating structure and token counts with tiktoken, and generating additional examples with GPT-4. Covers the decision matrix for when fine-tuning beats few-shot prompting or RAG, and the three-phase pipeline: dataset prep → job submission → evaluation.

## Applies If (ALL must hold)

- Output format or style is inconsistently produced by the base model despite prompt engineering (below 80% compliance)
- Domain-specific vocabulary causes incorrect or inconsistent terminology in base model outputs
- Current prompts are long (>500 tokens of examples) and reducing them via fine-tuning would cut latency and cost
- Deterministic output structure (strict JSON schemas) needed but base model produces it inconsistently
- Task clearly benefits from style/format fine-tuning rather than knowledge injection

## Skip If (ANY kills it)

- Goal is injecting new facts or knowledge — fine-tuning memorizes patterns, not facts; use RAG
- Fewer than 50 high-quality examples available — invest in data collection first
- Prompt engineering already achieves >90% quality — fine-tuning adds cost and operational overhead without meaningful gain
- Application uses many diverse tasks — a task-specific fine-tuned model can regress on other tasks
- Rapid iteration is needed — fine-tuning jobs take 30-60 minutes; prompt engineering allows instant iteration
- Sensitive data that must not be processed on OpenAI servers

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
