---
slug: db-comparison
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comparison of popular vector databases and selection guide for RAG systems.
content_id: "84e78516685b93d5"
tags: [vector-database, comparison, selection, rag, infrastructure]
---
# Vector Database Comparison

## Summary

**One-sentence:** Comparison of popular vector databases and selection guide for RAG systems.

**One-paragraph:** Comparison of popular vector databases and selection guide for RAG systems. Covers Qdrant, Weaviate, pgvector, Chroma, Pinecone, and Milvus across scale, hosting, filtering, and performance dimensions.

## Applies If (ALL must hold)

- Starting a new RAG or semantic search project and selecting the vector DB technology
- Migrating from a prototype DB (Chroma) to a production-grade one (Qdrant, Pinecone)
- Evaluating whether to add a separate vector DB or extend an existing PostgreSQL setup with pgvector
- Designing a multi-agent system where different agents use different retrieval backends

## Skip If (ANY kills it)

- Database is already selected and deployed; comparison analysis adds no value at this stage
- Corpus is < 10K vectors and latency is not critical — any DB works; pick the simplest
- Evaluating operational cost in isolation from query patterns; benchmarks without real queries are misleading

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
