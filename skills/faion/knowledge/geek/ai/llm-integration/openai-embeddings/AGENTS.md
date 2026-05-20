---
slug: openai-embeddings
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Generate dense vector representations of text using OpenAI embedding models and search them with cosine similarity.
content_id: "fd1d5e12774971c5"
tags: [embeddings, openai, rag, vector-search, batch-api]
---
# OpenAI Embeddings

## Summary

**One-sentence:** Generate dense vector representations of text using OpenAI embedding models and search them with cosine similarity.

**One-paragraph:** Generate dense vector representations of text using OpenAI embedding models and search them with cosine similarity. Two-phase workflow: (1) ingestion — chunk documents, embed in batch, upsert into vector store; (2) query — embed user query on demand, nearest-neighbor search, return top-k chunks. Use the Batch API for nightly re-indexing (50% cost reduction).

## Applies If (ALL must hold)

- Semantic search over a corpus (docs, tickets, FAQs) where keyword search misses intent
- Building or extending a RAG pipeline requiring dense vector retrieval
- Deduplication or clustering of text records at scale
- Classifying user input without a fine-tuned model
- Offline/async enrichment of large datasets (Batch API for 50% cost reduction)

## Skip If (ANY kills it)

- Real-time latency-sensitive paths where BM25 keyword index is fast enough
- Corpus fits in context — send documents directly to the LLM instead
- Exact string match is the requirement — embeddings are approximate
- Very short strings (1–3 words) — cosine similarity degrades; use BM25 or hybrid search

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

- parent skill: `geek/ai/llm-integration/`
