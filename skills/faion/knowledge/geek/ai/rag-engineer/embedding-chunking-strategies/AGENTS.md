---
slug: embedding-chunking-strategies
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Embedding models have token limits.
content_id: "358e2766d2dcfb36"
tags: [chunking, embeddings, rag, text-splitting, tokenization]
---
# Embedding Chunking Strategies

## Summary

**One-sentence:** Embedding models have token limits.

**One-paragraph:** Embedding models have token limits. Long documents must be split into chunks before embedding. The chunking strategy determines retrieval quality: wrong chunk size degrades both precision (too large — diluted context) and recall (too small — lost cross-sentence meaning).

## Applies If (ALL must hold)

- Any document corpus being ingested into a vector store for RAG retrieval.
- Documents longer than the embedding model's token limit (8191 for OpenAI models).
- When retrieval precision matters — chunk size tuning is the primary quality lever.
- Code search where function boundaries must be preserved.

## Skip If (ANY kills it)

- Short single-sentence texts already within token limits — chunking adds unnecessary overhead.
- Structured data (tables, databases) where semantic chunking destroys row integrity — use row-level embedding instead.

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
