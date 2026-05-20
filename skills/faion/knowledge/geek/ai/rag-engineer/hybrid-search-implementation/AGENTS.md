---
slug: hybrid-search-implementation
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Combines dense vector retrieval (semantic similarity) with sparse BM25 keyword retrieval, then fuses results using Reciprocal Rank Fusion (RRF) or linear alpha-weighted combination.
content_id: "de5ed8be08cb609a"
tags: [hybrid-search, implementation, vector-db, bm25, retrieval]
---
# Hybrid Search Implementation

## Summary

**One-sentence:** Combines dense vector retrieval (semantic similarity) with sparse BM25 keyword retrieval, then fuses results using Reciprocal Rank Fusion (RRF) or linear alpha-weighted combination.

**One-paragraph:** Combines dense vector retrieval (semantic similarity) with sparse BM25 keyword retrieval, then fuses results using Reciprocal Rank Fusion (RRF) or linear alpha-weighted combination. Covered implementations: Weaviate built-in hybrid, Qdrant prefetch+FusionQuery, Pinecone sparse-dense, Elasticsearch script_score, and a backend-agnostic HybridSearchService with dynamic alpha selection.

## Applies If (ALL must hold)

- RAG over technical documentation where exact identifiers matter alongside semantic meaning
- Legal, medical, or compliance corpora where specific terminology must match exactly
- Short queries (1-3 words) where semantic vectors alone underperform BM25
- Multilingual corpora where query and document languages may differ
- Upgrading a keyword-only search system to add semantic understanding without full replacement

## Skip If (ANY kills it)

- Purely conversational or conceptual queries with no exact-match requirements — dense-only is simpler
- Very small corpora (<5K documents) where BM25 overhead is not justified
- Real-time indexing of streaming documents where BM25 corpus statistics must be constantly rebuilt
- Latency-critical paths where running two retrieval pipelines doubles P99 latency beyond SLA

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
