---
slug: hybrid-search
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Hybrid search combines BM25 (sparse/keyword) and vector (dense/semantic) retrieval to maximize precision and recall.
content_id: "53cf610dc1ea44b1"
tags: [hybrid-search, rag, vector-search, bm25, fusion]
---
# Hybrid Search: Combining BM25 and Vector Retrieval

## Summary

**One-sentence:** Hybrid search combines BM25 (sparse/keyword) and vector (dense/semantic) retrieval to maximize precision and recall.

**One-paragraph:** Hybrid search combines BM25 (sparse/keyword) and vector (dense/semantic) retrieval to maximize precision and recall. Use Reciprocal Rank Fusion (RRF) as the default fusion method — it requires no score normalization and works across different score scales. Add a cross-encoder reranker (Cohere, bge-reranker-v2-m3) only if precision is still insufficient after hybrid. Benchmarks: hybrid + reranking achieves 87% relevant docs in top-10 vs 62% BM25-only and 71% vector-only.

## Applies If (ALL must hold)

- RAG pipeline serves queries that mix natural language and exact terms (product codes, error messages, legal statute numbers, names)
- Pure vector search precision is inadequate (less than 75% relevant results in top-10) and queries include specific keywords that should match exactly
- Enterprise search over technical documentation where users alternate between concept searches and exact string lookups
- Production system where +15% precision gain justifies ~20% additional latency and complexity
- Replacing an existing BM25-only search with semantic capability without discarding keyword matching

## Skip If (ANY kills it)

- Corpus is less than 1,000 documents — pure vector search is fast enough and simpler to operate
- All queries are conversational/semantic with no exact term requirements — pure vector search suffices; hybrid adds latency without benefit
- Latency budget is under 20ms — hybrid search (parallel BM25 + vector + fusion) typically costs 40-100ms
- Infrastructure is Elasticsearch-only — native kNN + BM25 in ES is effective without adding a second vector DB

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
