---
slug: embedding-generation
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Converts text chunks into dense vectors using an embedding model so they can be stored in a vector database and retrieved by semantic similarity.
content_id: "8ee3fcacee25f7f6"
tags: [embeddings, vectors, semantic-search, rag, indexing]
---
# Embedding Generation

## Summary

**One-sentence:** Converts text chunks into dense vectors using an embedding model so they can be stored in a vector database and retrieved by semantic similarity.

**One-paragraph:** Converts text chunks into dense vectors using an embedding model so they can be stored in a vector database and retrieved by semantic similarity. The indexing step takes {id, text} chunk dicts, batches them, and returns {id, embedding, model, dimensions} dicts. The query step embeds the user query with the same model and measures cosine similarity against the stored vectors.

## Applies If (ALL must hold)

- Building the indexing step of any RAG pipeline (chunks to vectors).
- Implementing semantic search over a document corpus.
- Text clustering, deduplication by semantic similarity, or recommendation systems.
- Evaluating embedding model options for a new project before committing to a provider.
- Optimizing an existing embedding pipeline for cost, latency, or quality.

## Skip If (ANY kills it)

- Exact-string keyword search is sufficient — embeddings add cost/latency with no precision gain for exact matches.
- Very short texts (less than 10 tokens) — BM25 outperforms semantic similarity at this scale.
- Corpus is in a low-resource language without a multilingual model — embeddings may produce near-random vectors.
- Storage budget is constrained and 1536-3072 dimension vectors would overflow it — benchmark with reduced dimensions first.

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
