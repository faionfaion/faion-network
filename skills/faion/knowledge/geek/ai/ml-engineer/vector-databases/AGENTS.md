---
slug: vector-databases
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Vector databases solve approximate nearest neighbor (ANN) search at scale — finding semantically similar items without exact keyword matching.
content_id: "14759711afc1940a"
tags: [vector-databases, rag, semantic-search, embeddings, similarity-search]
---
# Vector Databases

## Summary

**One-sentence:** Vector databases solve approximate nearest neighbor (ANN) search at scale — finding semantically similar items without exact keyword matching.

**One-paragraph:** Vector databases solve approximate nearest neighbor (ANN) search at scale — finding semantically similar items without exact keyword matching. The choice of database, index type, and quantization strategy determines recall accuracy, query latency, memory usage, and operational complexity. Wrong choices are expensive to migrate later.

## Applies If (ALL must hold)

- Building a RAG pipeline that needs semantic similarity search
- Storing and querying document embeddings at scale (10K+ documents)
- Implementing multi-tenant knowledge bases with namespace isolation
- Replacing keyword-only search with semantic or hybrid search
- Benchmarking or migrating between vector DB providers

## Skip If (ANY kills it)

- Dataset fits in memory and has fewer than ~1,000 documents — use in-process numpy similarity instead
- Requirement is pure exact-match lookup — a relational DB or Redis suffices
- The application already uses Elasticsearch with kNN and a rewrite is not justified
- Prototyping a single-user tool with no persistence requirement — Chroma in-memory is enough

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
