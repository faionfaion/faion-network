---
slug: rag-eval-retrieval-metrics
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Retrieval metrics measure whether the RAG system fetches the right documents before generation happens.
content_id: "85295da758e470f5"
tags: [rag, evaluation, retrieval, metrics, information-retrieval]
---
# RAG Retrieval Quality Metrics

## Summary

**One-sentence:** Retrieval metrics measure whether the RAG system fetches the right documents before generation happens.

**One-paragraph:** Retrieval metrics measure whether the RAG system fetches the right documents before generation happens. The five core metrics — Precision@K, Recall@K, MRR, NDCG@K, and Hit Rate — are pure-Python computations with zero API cost and should run on every test evaluation.

## Applies If (ALL must hold)

- Measuring whether the retriever returns relevant documents for a labeled test set (ground-truth relevant doc IDs available).
- Selecting or tuning the retrieval top-K — Precision@K and Recall@K give direct feedback on the K parameter.
- Ranking-quality comparison between two retrieval strategies (e.g., dense vs. hybrid) — use NDCG@K for graded relevance.
- CI quality gate: fail a deployment if Hit Rate drops below 0.90 or Precision@5 drops below 0.70.
- Diagnosing a generation quality problem: if faithfulness is low but Precision@K is high, the problem is the generator, not the retriever.

## Skip If (ANY kills it)

- When no ground-truth relevant doc IDs exist — Precision@K, Recall@K, MRR, and NDCG@K all require labeled sets; collect labels via human annotation or synthetic test-set generation before applying these metrics.
- Real-time per-query scoring in production — these metrics require a labeled test set comparison, not a single live query; for online monitoring use generation-side signals (faithfulness sampling) instead.
- Replacing generation metrics — high Precision@K says nothing about whether the generator produces faithful, relevant answers; always pair with generation metrics.

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
