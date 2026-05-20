---
slug: llm-decision-framework
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints.
content_id: "4e0a4a0af006e59f"
tags: [llm-architecture, rag, fine-tuning, decision-framework, cost-optimization]
---
# LLM Decision Framework

## Summary

**One-sentence:** A systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints.

**One-paragraph:** A systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints. Always score prompting first before investing in retrieval or training infrastructure.

## Applies If (ALL must hold)

- At the start of any AI feature design: choose the right architecture before writing code
- Evaluating whether to augment an existing LLM feature
- During cost optimization: deciding whether a fine-tuned cheaper model can replace an expensive general model
- When accuracy is inadequate: diagnosing if the root cause is knowledge, style, or reasoning
- Business justification for AI budget: quantify cost/benefit before committing

## Skip If (ANY kills it)

- Prototype needed in under a day — default to prompt engineering, evaluate later
- Decision already made by stakeholders — use the framework to document trade-offs, not re-litigate
- Task is purely generative (creative writing) — retrieval and fine-tuning do not apply
- No eval data exists — the framework requires measurable accuracy targets; skip until measurable

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
