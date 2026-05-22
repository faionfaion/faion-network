---
slug: hybrid-search-implementation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Ships a production HybridSearchService that wires dense + sparse legs in Weaviate / Qdrant / Pinecone / Elasticsearch with RRF or alpha fusion and parallel leg execution.
content_id: "de5ed8be08cb609a"
complexity: deep
produces: code
est_tokens: 4500
tags: [hybrid-search, implementation, vector-db, bm25, retrieval]
---
# Hybrid Search Implementation

## Summary

**One-sentence:** Ships a production HybridSearchService that wires dense + sparse legs in Weaviate / Qdrant / Pinecone / Elasticsearch with RRF or alpha fusion and parallel leg execution.

**One-paragraph:** Combines dense vector retrieval (semantic similarity) with sparse BM25 keyword retrieval, then fuses results using Reciprocal Rank Fusion (RRF) or linear alpha-weighted combination. Covered implementations: Weaviate built-in hybrid, Qdrant prefetch+FusionQuery, Pinecone sparse-dense, Elasticsearch script_score, and a backend-agnostic HybridSearchService with dynamic alpha selection. Each backend has its own pre-computation, tokenisation, and convention quirks that the implementation must respect.

**Ефективно для:** інженерів, які мають готовий decision (hybrid-search-basics) і потрібно довести його до production-grade сервісу з конкретною vector DB.

## Applies If (ALL must hold)

- RAG over technical documentation where exact identifiers matter alongside semantic meaning.
- Legal, medical, or compliance corpora where specific terminology must match exactly.
- Short queries (1-3 words) where semantic vectors alone underperform BM25.
- The target store is Weaviate / Qdrant / Pinecone / Elasticsearch (covered backends).

## Skip If (ANY kills it)

- Purely conversational queries with no exact-match requirements — dense-only is simpler.
- Very small corpora (&lt;5k documents) — BM25 overhead is not justified.
- Real-time streaming indexing where BM25 statistics must be constantly rebuilt.
- Latency-critical paths where running two pipelines doubles P99 latency beyond SLA.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Chosen hybrid-search config | YAML | hybrid-search-basics |
| Vector store credentials | env vars | infra |
| BM25 encoder (if Pinecone) | serialised pickle | pre-training step |
| Labeled query set | JSONL | rag-eval-test-set-generation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/hybrid-search-basics` | Defines the config this implements. |
| `geek/ai/rag-engineer/vector-database-setup` | Backend choice + index schema. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: weaviate alpha, qdrant prefetch, pinecone bm25encoder, prefer-RRF, measure-alpha, fetch-2-3x | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for HybridSearchService.search() result | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: language tokeniser mismatch, stale BM25Encoder, type mix Qdrant/Pinecone, serial leg execution | ~800 |
| `content/04-procedure.xml` | medium | 6-step build procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree picking native-hybrid vs client-fusion path | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick backend and config flavour | sonnet | Multi-criteria. |
| Write adapter code | sonnet | Per-backend API specifics. |
| Wire parallel leg execution | haiku | Mechanical asyncio/threadpool. |
| Debug score-scale issues | opus | Cross-leg numerical reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid_search_service.py.tmpl` | Backend-agnostic HybridSearchService skeleton with async parallel legs and RRF fusion. |
| `templates/weaviate-hybrid.py` | Weaviate native hybrid() call example. |
| `templates/qdrant-hybrid.py` | Qdrant prefetch + FusionQuery example. |
| `templates/_smoke-test.py` | Minimum runnable test using the agnostic service. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-search-implementation.py` | Validates a search-result JSON against schema. | Pre-commit; CI. |

## Related

- [[hybrid-search-basics]]
- [[vector-database-setup]]
- [[reranking-pipeline-integration]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the integration path: root question — "Does the target store have native server-side hybrid?". Branches lead to native-hybrid (Weaviate/Qdrant), client-fusion (Elasticsearch/custom), or sparse-dense (Pinecone with BM25Encoder). Each leaf references a rule from 01-core-rules.xml.
