---
slug: db-qdrant
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Qdrant outperforms Pinecone at production scale for self-hosted workloads (41 QPS @ 50M vectors) and exposes HNSW tuning knobs unavailable in Chroma.
content_id: "a6853d34911bb8d1"
tags: [vector-database, qdrant, production, rag, hybrid-search]
---
# Qdrant Vector Database

## Summary

**One-sentence:** Qdrant outperforms Pinecone at production scale for self-hosted workloads (41 QPS @ 50M vectors) and exposes HNSW tuning knobs unavailable in Chroma.

**One-paragraph:** Qdrant outperforms Pinecone at production scale for self-hosted workloads (41 QPS @ 50M vectors) and exposes HNSW tuning knobs unavailable in Chroma. Scalar quantization halves RAM without measurable recall loss for most corpora; binary quantization achieves 32x reduction for high-dimensional models. Built-in sparse-vector support eliminates the need for a separate keyword search engine in hybrid pipelines.

## Applies If (ALL must hold)

- Standing up a production self-hosted vector store (Docker or Kubernetes)
- RAG pipelines needing payload-level filtering alongside vector similarity
- Systems requiring hybrid dense+sparse (BM25) search without a separate engine
- High-volume indexing (>1M vectors) with memory constraints
- Multi-modal retrieval (one point stores text + image vectors as named vectors)
- Pipelines requiring point-level snapshots and incremental backups

## Skip If (ANY kills it)

- Prototype/local dev with <50K vectors and no filtering needs — Chroma is simpler and zero-config
- Existing PostgreSQL stack where pgvector extension is already present
- Teams that need a fully managed SaaS with zero infra ops — use Qdrant Cloud or Pinecone
- Requirements for GraphQL or Weaviate-style schema-first data modeling

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
