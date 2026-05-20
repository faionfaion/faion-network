---
slug: vector-db-setup-dev
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spin up any major vector database (Qdrant, Weaviate, Milvus, pgvector, Pinecone, Chroma) locally via Docker one-liners or pip install, connect a Python client, create a collection, and verify the stack is functional before writing pipeline code.
content_id: "03cb64d3f85bd005"
tags: [vector-database, docker, development, qdrant, weaviate]
---
# Vector Database Development Setup

## Summary

**One-sentence:** Spin up any major vector database (Qdrant, Weaviate, Milvus, pgvector, Pinecone, Chroma) locally via Docker one-liners or pip install, connect a Python client, create a collection, and verify the stack is functional before writing pipeline code.

**One-paragraph:** Spin up any major vector database (Qdrant, Weaviate, Milvus, pgvector, Pinecone, Chroma) locally via Docker one-liners or pip install, connect a Python client, create a collection, and verify the stack is functional before writing pipeline code.

## Applies If (ALL must hold)

- Starting a new RAG pipeline and need a vector store to develop against.
- Evaluating a database before committing to a production deployment.
- Running integration tests that require a real (not mocked) vector database.
- Migrating from Chroma in-memory to a persistent database during prototyping.

## Skip If (ANY kills it)

- Proof-of-concept with fewer than 10K documents — use Chroma in-memory or pgvector on an existing Postgres; no Docker needed.
- Production deployment — use the vector-db-setup-prod methodology instead; dev defaults are not hardened.
- The bottleneck is embedding quality or chunking strategy — fix those upstream before adding database complexity.

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
