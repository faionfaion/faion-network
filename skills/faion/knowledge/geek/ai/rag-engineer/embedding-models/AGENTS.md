---
slug: embedding-models
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Different models trade off quality, cost, context length, and language coverage.
content_id: "ef33781808b6be25"
tags: [embeddings, models, batch-processing, api, rag]
---
# Embedding Models

## Summary

**One-sentence:** Different models trade off quality, cost, context length, and language coverage.

**One-paragraph:** Different models trade off quality, cost, context length, and language coverage. text-embedding-3-large leads MTEB benchmarks for English but costs 6x more than text-embedding-3-small and stores 2x more per vector. Local models (BGE-M3) are free and support multilingual + sparse output for hybrid search, but require GPU for production throughput. Cohere v3's input_type asymmetry (search_document vs search_query) improves retrieval NDCG by 5-10% over generic mode. Model selection is a load-bearing decision: a model change invalidates the entire index.

## Applies If (ALL must hold)

- Selecting an embedding model at the start of a RAG project (pin model before indexing)
- Benchmarking multiple providers to find the best price/quality ratio for a specific corpus
- Migrating an index from one model to another (e.g., ada-002 → text-embedding-3-large)
- Building code-search RAG where general-purpose models underperform (use voyage-code-3 or BGE-M3)
- Processing multilingual corpora where English-only models degrade retrieval quality

## Skip If (ANY kills it)

- Corpus is already indexed and migration cost outweighs quality gain — benchmark first
- Latency budget is <20ms — API models add network RTT; local models add model-load overhead
- Fully offline/air-gapped deployment with no GPU — local models on CPU are slow for batches >1k

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
