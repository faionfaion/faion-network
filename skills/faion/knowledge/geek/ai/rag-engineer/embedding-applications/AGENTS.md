---
slug: embedding-applications
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Benchmarking, vector database integration, and production usage patterns for embedding models.
content_id: "0e2203ee9405c78b"
tags: [embeddings, benchmarking, vector-databases, rag, retrieval]
---
# Embedding Applications

## Summary

**One-sentence:** Benchmarking, vector database integration, and production usage patterns for embedding models.

**One-paragraph:** Benchmarking, vector database integration, and production usage patterns for embedding models. Covers MTEB leaderboard analysis, custom benchmarking against labeled retrieval datasets, speed profiling, and safe integration with Qdrant, pgvector, Weaviate, and other vector databases.

## Applies If (ALL must hold)

- Building or benchmarking a RAG retrieval stage (model selection, quality gates).
- Choosing between embedding providers (OpenAI, Cohere, open-source) for a new project.
- Running regression checks after switching embedding models or chunking strategy.
- Populating or migrating a vector database (Qdrant, pgvector, Chroma, Weaviate).
- Validating retrieval quality against a labeled dataset before going to production.

## Skip If (ANY kills it)

- The task is purely generative — no retrieval component needed.
- Dataset is fewer than 50 query/document pairs; MTEB-style benchmarking yields noise at that scale.
- Latency budget is so tight that embedding overhead is unacceptable (consider keyword search instead).
- Team lacks ground-truth relevance labels; benchmark numbers will mislead rather than guide.

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
