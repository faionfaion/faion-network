---
slug: rag-eval-strategy
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: RAG evaluation strategy defines which metrics to run, when to run them, how to sample to control LLM-judge costs, and how to set explicit numeric quality gates.
content_id: "3f280a91a2b13122"
tags: [rag, evaluation, quality-gates, cost-optimization, strategy]
---
# RAG Evaluation Strategy

## Summary

**One-sentence:** RAG evaluation strategy defines which metrics to run, when to run them, how to sample to control LLM-judge costs, and how to set explicit numeric quality gates.

**One-paragraph:** RAG evaluation strategy defines which metrics to run, when to run them, how to sample to control LLM-judge costs, and how to set explicit numeric quality gates. The core principle: retrieval metrics (free, run always) + generation metrics (expensive, run on 10-20% sample) + explicit numeric thresholds before deployment.

## Applies If (ALL must hold)

- Before adding any RAG evaluation — use this methodology to decide which metrics to implement first.
- Before deploying a new retriever or generator — derive deployment quality gate thresholds from this strategy.
- When LLM-judge evaluation costs are becoming a concern — apply cost-tier sampling rules here.
- When a metric is trending downward in production — use evaluation stage guidance to escalate from Hit Rate (cheap) to full RAGAS suite.

## Skip If (ANY kills it)

- After the pipeline is already built with hardcoded metrics — at that point read rag-eval-retrieval-metrics and rag-eval-generation-metrics for the specific implementations.
- When evaluating a single query interactively — strategy is for systematic batch evaluation, not one-off debugging.

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

- parent skill: `geek/ai/rag-engineer/`
