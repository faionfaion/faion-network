---
slug: db-chroma
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Embedded SQLite/HNSW vector store for RAG prototyping with zero infrastructure and idempotent get_or_create_collection ingestion; single-process only.
content_id: "0aedaad3bbf2f5c1"
complexity: medium
produces: code
est_tokens: 3400
tags: [vector-database, chroma, rag, prototyping, embedding]
---
# Chroma Vector Database

## Summary

**One-sentence:** Embedded SQLite/HNSW vector store for RAG prototyping with zero infrastructure and idempotent `get_or_create_collection` ingestion; single-process only.

**One-paragraph:** Chroma runs in-process (PersistentClient backed by SQLite + HNSW). Distance metric is set at collection creation and cannot be changed without recreating. IDs are strings (integers must be stringified). `get_or_create_collection` makes re-runs idempotent. Integrates directly with LangChain and LlamaIndex. Use Chroma for dev / eval / single-developer prototypes; promote to Qdrant or Pinecone before crossing 1M vectors, multi-tenant SaaS, or multi-process write workloads.

**Ефективно для:** Solopreneur prototyping a RAG pipeline locally — closes the gap between "open notebook" and a persistent vector store without Docker overhead.

## Applies If (ALL must hold)

- Single-developer prototype OR CI eval harness OR notebook-based research.
- Corpus < 1M vectors.
- Single-process write workload; no concurrent writers.
- Acceptable to migrate to a production vector store before scale-up.

## Skip If (ANY kills it)

- Production deployment with >1M vectors — load [[db-qdrant]] or [[db-weaviate]].
- Multi-tenant SaaS — Chroma lacks tenant isolation.
- High-concurrency writes — SQLite corrupts under concurrent writers.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| chromadb | python pkg | `pip install chromadb` |
| Persistence dir path | filesystem path | application config |
| Embedding function | callable or chromadb embedding fn | matches retrieval |
| Distance metric | "cosine" / "l2" / "ip" | decided once at collection creation |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/embedding-generation` | Embedding function semantics. |
| `geek/ai/rag-engineer/db-comparison` | Why Chroma vs Qdrant/Weaviate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: metric-at-creation, string IDs, get_or_create idempotent, single-process writes, persistence path | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for ChromaStore output: collection name, upsert ack, search hits with metadata | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: multi-process writes, integer IDs, metric change, missing persistence | ~700 |
| `content/04-procedure.xml` | medium | 5-step setup → embed → upsert → search → backup | ~600 |
| `content/06-decision-tree.xml` | essential | Routes scale + tenancy + concurrency to Chroma vs Qdrant vs pgvector | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `setup` | haiku | Mechanical client creation. |
| `bulk-upsert` | haiku | I/O. |
| `query-debug` | sonnet | Result inspection on poor recall. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chroma_store.py` | ChromaStore wrapper with metric pinning, string IDs, idempotent upsert. |
| `templates/chroma-schema.json` | JSON Schema for ChromaStore search/upsert payloads. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-chroma.py` | Verify ChromaStore payload schema; check metric set; check IDs are strings. | After upsert / before commit. |

## Related

- [[db-qdrant]] · [[db-weaviate]] · [[db-comparison]] · [[rag-architecture]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by corpus size, tenancy, and concurrency to Chroma, Qdrant, Weaviate, or pgvector. Use it before instantiating a client so the scale-up path is explicit.
