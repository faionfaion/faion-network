---
slug: embedding-caching
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Embedding the same text twice wastes API cost and latency.
content_id: "484df2202087698b"
tags: [embeddings, caching, redis, rag, cost-reduction]
---
# Embedding Caching Patterns

## Summary

**One-sentence:** Embedding the same text twice wastes API cost and latency.

**One-paragraph:** Embedding the same text twice wastes API cost and latency. Cache embeddings by a model-namespaced hash of the text. In production, use Redis with a 30-day TTL. Typical RAG workloads see 70-90% cache hit rates on repeat queries and re-ingested documents.

## Applies If (ALL must hold)

- High-volume embedding workloads where documents or queries repeat across requests.
- RAG systems with incremental ingestion — new documents added to a mostly-stable corpus.
- Production systems where embedding API cost is measurable.
- Any workload calling the same embedding model for overlapping text sets.

## Skip If (ANY kills it)

- One-time batch ingestion of a fully unique corpus — cache miss rate will be 100% and cache adds overhead.
- Streaming real-time embeddings where latency matters more than cost — Redis round-trip may exceed the embedding API latency for small models.

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
