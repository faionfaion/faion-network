---
slug: db-chroma
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Chroma removes all infrastructure friction for RAG prototyping: one Python import, one directory, zero Docker.
content_id: "0aedaad3bbf2f5c1"
tags: [vector-database, chroma, rag, prototyping, embedding]
---
# Chroma Vector Database

## Summary

**One-sentence:** Chroma removes all infrastructure friction for RAG prototyping: one Python import, one directory, zero Docker.

**One-paragraph:** Chroma removes all infrastructure friction for RAG prototyping: one Python import, one directory, zero Docker. Its get_or_create_collection pattern makes ingestion re-runs idempotent. It integrates directly with LangChain and LlamaIndex, covering the common development → eval → staging path before promoting to Qdrant or Pinecone for production.

## Applies If (ALL must hold)

- Local development and prototyping of RAG pipelines (no external server needed)
- Single-developer projects or small teams where operational simplicity trumps scale
- Running evaluation harnesses in CI where spinning up Qdrant/Weaviate adds friction
- Notebook-based research and experimentation with embeddings
- Applications needing an embedded vector store with zero infrastructure (SQLite role)

## Skip If (ANY kills it)

- Production deployments with >1M vectors — Chroma performance degrades and lacks Qdrant's tuning knobs
- Multi-tenant SaaS — Chroma has no native access control or tenant isolation
- High-concurrency write workloads — PersistentClient uses SQLite; concurrent writes from multiple processes corrupt the DB
- Multi-node horizontal scaling — Chroma does not support distributed deployment

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
