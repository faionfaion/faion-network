---
slug: embeddings-model-selection
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choose an embedding model by matching use case (RAG, search, clustering, classification), constraints (budget, latency, privacy, language), and provider capabilities (Matryoshka dimensions, quantization, asymmetric input types).
content_id: "9cc29e2b8825e050"
tags: [embeddings, model-selection, rag, semantic-search, vector]
---
# Text Embedding Model Selection

## Summary

**One-sentence:** Choose an embedding model by matching use case (RAG, search, clustering, classification), constraints (budget, latency, privacy, language), and provider capabilities (Matryoshka dimensions, quantization, asymmetric input types).

**One-paragraph:** Choose an embedding model by matching use case (RAG, search, clustering, classification), constraints (budget, latency, privacy, language), and provider capabilities (Matryoshka dimensions, quantization, asymmetric input types). MTEB scores are general — always benchmark on your own data before committing.

## Applies If (ALL must hold)

- Starting a new semantic search or RAG project and need to pick an embedding provider.
- Evaluating whether to switch from one embedding model to another.
- Choosing between cloud API and local/self-hosted models.
- Optimizing an existing system for cost, latency, or quality.

## Skip If (ANY kills it)

- Exact keyword or structured data lookup — BM25 or SQL is faster and more precise.
- Tiny corpora under 500 docs — cosine similarity across all docs is trivially fast without indexing.
- When the domain is highly specialized and no domain-adapted model exists — consider fine-tuning or BM25 fallback first.
- Real-time streaming data where batch embedding latency blocks the pipeline.

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
