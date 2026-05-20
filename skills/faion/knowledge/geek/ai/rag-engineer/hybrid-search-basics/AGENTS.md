---
slug: hybrid-search-basics
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Hybrid search combines dense vector search (semantic similarity) with sparse lexical search (BM25/keyword) and fuses the ranked results using Reciprocal Rank Fusion (RRF) or weighted linear combination.
content_id: "08c882d10ff0457e"
tags: [hybrid-search, bm25, rrf, fusion, retrieval]
---
# Hybrid Search Basics

## Summary

**One-sentence:** Hybrid search combines dense vector search (semantic similarity) with sparse lexical search (BM25/keyword) and fuses the ranked results using Reciprocal Rank Fusion (RRF) or weighted linear combination.

**One-paragraph:** Hybrid search combines dense vector search (semantic similarity) with sparse lexical search (BM25/keyword) and fuses the ranked results using Reciprocal Rank Fusion (RRF) or weighted linear combination. RRF is the default fusion strategy. The balance between semantic and keyword signals is controlled by an alpha parameter (1.0 = pure semantic, 0.0 = pure keyword) that should be tuned per domain on a labeled query set.

## Applies If (ALL must hold)

- Document corpus contains exact technical terms, product codes, or names that semantic search misses.
- Domain is legal, medical, or compliance-heavy where precise phrase matching is required.
- User queries mix conceptual intent with specific identifiers.
- Pure vector search recall is below acceptable threshold on benchmark query set.
- System uses Qdrant, Weaviate, or Elasticsearch — all support hybrid natively.

## Skip If (ANY kills it)

- Corpus is purely natural-language prose with no technical identifiers — pure semantic suffices.
- Latency budget is very tight (< 100ms) — hybrid adds BM25 scoring overhead.
- Corpus is too small (< 500 documents) — BM25 gains are negligible at small scale.
- Already using a cross-encoder reranker over broad vector retrieval — reranker compensates for keyword misses.

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
