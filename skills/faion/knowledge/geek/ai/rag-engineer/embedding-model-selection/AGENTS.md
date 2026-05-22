---
slug: embedding-model-selection
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Text embeddings are numerical vector representations of text that capture semantic meaning.
content_id: "bf77ef61c48ded16"
tags: [embeddings, rag, model-selection, vector-search, openai]
---
# Embedding Model Selection for RAG

## Summary

**One-sentence:** Text embeddings are numerical vector representations of text that capture semantic meaning.

**One-paragraph:** Text embeddings are numerical vector representations of text that capture semantic meaning. Selecting the correct model requires balancing quality, cost, token limits, language coverage, and inference latency against the specific RAG workload.

## Applies If (ALL must hold)

- Any task requiring semantic similarity between texts (RAG retrieval, deduplication, clustering, classification without labeled data).
- Building the ingestion step of a RAG pipeline — every chunk must be embedded before storage.
- Multilingual search where query and document languages may differ (use multilingual models).
- Cost optimization decisions: choosing between API-based and local embedding models.
- Starting a new vector index — before any ingestion begins.

## Skip If (ANY kills it)

- Exact keyword matching is sufficient — embeddings add cost and latency with no semantic benefit.
- The corpus is fewer than 500 texts that will never change — a one-time TF-IDF matrix is simpler and cheaper.
- You need real-time streaming embeddings at sub-10ms latency — API round-trips make this infeasible; need a local model.
- The domain is highly specialized (chemistry, genomics) and no domain-adapted model exists — embeddings will produce poor semantic similarity.

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
