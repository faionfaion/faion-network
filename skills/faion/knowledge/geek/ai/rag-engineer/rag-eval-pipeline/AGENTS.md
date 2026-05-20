---
slug: rag-eval-pipeline
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A complete evaluation pipeline runs each test-set question through the production RAG pipeline, computes retrieval metrics (precision@5, recall@5, MRR, hit rate) and generation metrics (faithfulness, answer relevance, context relevance) via LLM scoring or RAGAS, aggregates results, and exports to JSON.
content_id: "b69017d80525526d"
tags: [rag, evaluation, pipeline, ragas, metrics]
---
# RAG Evaluation Pipeline

## Summary

**One-sentence:** A complete evaluation pipeline runs each test-set question through the production RAG pipeline, computes retrieval metrics (precision@5, recall@5, MRR, hit rate) and generation metrics (faithfulness, answer relevance, context relevance) via LLM scoring or RAGAS, aggregates results, and exports to JSON.

**One-paragraph:** A complete evaluation pipeline runs each test-set question through the production RAG pipeline, computes retrieval metrics (precision@5, recall@5, MRR, hit rate) and generation metrics (faithfulness, answer relevance, context relevance) via LLM scoring or RAGAS, aggregates results, and exports to JSON. Human review of the aggregated report is required before any pipeline change is merged to production.

## Applies If (ALL must hold)

- Before deploying a RAG system to production — establishing baseline quality scores.
- After any pipeline change (chunking strategy, top-K, model swap) to detect regressions.
- When the test set has at least 20 questions — smaller sets are dominated by statistical noise.
- Weekly batch evaluation on a sampled subset in production to catch quality drift.

## Skip If (ANY kills it)

- High-frequency real-time evaluation of every query in production — use lightweight metrics (latency, hit rate, user signals) instead; reserve LLM eval for sampled batches.
- When ground truth answers are unavailable — only faithfulness and answer_relevancy are computable without ground truth; RAGAS context_precision and context_recall require ground truth.

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
