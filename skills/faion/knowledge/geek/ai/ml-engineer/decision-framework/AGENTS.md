---
slug: decision-framework
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured decision process for selecting the right AI approach (prompt engineering, RAG, fine-tuning) and the right model tier for a given task.
content_id: "80370396310c8ed4"
tags: [decision-framework, model-selection, rag, fine-tuning, cost-optimization]
---
# ML/AI Decision Framework

## Summary

**One-sentence:** A structured decision process for selecting the right AI approach (prompt engineering, RAG, fine-tuning) and the right model tier for a given task.

**One-paragraph:** A structured decision process for selecting the right AI approach (prompt engineering, RAG, fine-tuning) and the right model tier for a given task. Applies a progressive enhancement strategy: start with prompting → add RAG when external data is needed → add fine-tuning only when behavioral specialization is required at scale. Implements complexity-based model routing to reduce cost by 40-60%.

## Applies If (ALL must hold)

- Starting a new AI feature and choosing between prompting, RAG, or fine-tuning
- Monthly API spend has grown and you suspect model over-selection
- A model is deprecated or a cheaper/faster alternative has appeared
- Different pipeline stages require different capability/cost trade-offs
- Evaluating whether to switch providers for a specific workload

## Skip If (ANY kills it)

- The task is trivial and the model is already decided — don't over-engineer
- A deadline is imminent — pick the safe default (Claude Sonnet or GPT-4o) and optimize later
- Purely creative tasks (marketing copy, story generation) — model quality differences are subjective; user preference testing matters more than a framework

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
