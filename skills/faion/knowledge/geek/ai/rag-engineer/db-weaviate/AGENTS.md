---
slug: db-weaviate
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Vector database with knowledge graph capabilities and hybrid search.
content_id: "5e5242820eb0ca4f"
tags: [vector-database, knowledge-graphs, hybrid-search, graphql, rag]
---
# Weaviate Vector Database

## Summary

**One-sentence:** Vector database with knowledge graph capabilities and hybrid search.

**One-paragraph:** Vector database with knowledge graph capabilities and hybrid search. Weaviate excels at knowledge graphs and hybrid search (semantic + keyword). GraphQL native. Best for knowledge graphs at 10M+ vector scale with self or cloud hosting.

## Applies If (ALL must hold)

- Knowledge graph capabilities are needed: entities with cross-references (Author → Document → Topic).
- Native hybrid search (vector + BM25) is required without client-side fusion code.
- GraphQL-based querying fits the team's existing tooling or API gateway.
- Corpus contains multi-modal data (text + images) — Weaviate supports multi-vector objects.
- Self-hosted deployment on Kubernetes at 10M–100M vector scale.

## Skip If (ANY kills it)

- Simple RAG prototype with no graph relationships — Chroma or Qdrant are simpler to set up.
- Team is unfamiliar with GraphQL; prefer Qdrant (REST/gRPC) for API simplicity.
- Payload filtering at high cardinality is the primary concern — Qdrant's payload filter performance exceeds Weaviate's at scale.
- Cost-sensitive managed deployment at 1B+ vectors — Pinecone or Milvus have lower per-vector managed pricing.

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
