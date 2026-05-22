---
slug: openai-embeddings
tier: geek
group: ai
domain: llm-integration
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates an ingestion+query embedding pipeline (chunk, embed, upsert, search) with model+dims pinning, normalization, and Batch-API correlation by custom_id.
content_id: "2f1b0c4a8e6d2937"
complexity: medium
produces: code
est_tokens: 4000
tags: [embeddings, openai, rag, vector-search, batch-api]
---
# OpenAI Embeddings

## Summary

**One-sentence:** Two-phase embedding pipeline (ingest + query) that pins model+dimensions, chunks at semantic boundaries, stores text-with-vector, and uses Batch API only where the 24-hour window is acceptable.

**One-paragraph:** Generates dense vector representations of text using OpenAI embedding models and searches them with cosine similarity. Ingestion: chunk documents, embed in batch, upsert into vector store. Query: embed (rewritten) user query on demand, nearest-neighbor search, return top-k chunks. Pins model and `dimensions` across ingestion and query — mixing them yields meaningless similarity with no error.

**Ефективно для:** RAG-інженера, що ставить семантичний пошук поверх корпусу — закриває цикл chunk → embed → search із контрактом по моделі та dims.

## Applies If (ALL must hold)

- Semantic search over a corpus where keyword search misses intent.
- Building or extending a RAG pipeline requiring dense vector retrieval.
- Deduplication or clustering of text records at scale.
- Classifying user input without a fine-tuned model.
- Offline / async enrichment is acceptable (Batch API gives 50% cost reduction).

## Skip If (ANY kills it)

- Real-time latency-sensitive paths where BM25 keyword index is fast enough.
- Corpus fits in context — send documents directly to the LLM instead.
- Exact string match is the requirement — embeddings are approximate.
- Very short strings (1–3 words) — cosine similarity degrades; use BM25 or hybrid search.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source documents | text/markdown/html | content store, S3, DB |
| Chunking strategy | config | `chunking-strategies` methodology |
| Vector store handle | client | pinecone / weaviate / pgvector |
| Model + dims pin | config | shared between ingestion and query |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/chunking-strategies` | Provides semantic-boundary chunker that feeds the embedder. |
| `geek/ai/llm-integration/openai-chat-completions` | For optional query-expansion call. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: model+dims pin, semantic chunking + overlap, store-text-with-vector, query-expansion, batch-correlation, no-PII-shared-store | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one embed-record (custom_id, model, dims, vector_len, source_hash) + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair: dims-mismatch, silent-truncation, batch-fifo-assumption, pii-leak, query-on-raw-message | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: pin config → chunk → embed (batch or sync) → upsert → search → return top-k | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Batch vs sync, small vs large model, full vs reduced dimensions | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `chunk-text` | haiku | Pure mechanical split; no judgment. |
| `expand-query` | sonnet | Rewrites short queries for recall; needs language judgment. |
| `recall-eval` | opus | Cross-corpus retrieval audit when recall drops. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embed-and-search.py` | Reusable embed() + cosine() + top_k() functions with model+dims pinning. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-embeddings.py` | Validate an embed-record JSON matches the output contract (custom_id, model, dims, vector_len, source_hash). | Post-embed pipeline; nightly index audit. |

## Related

- [[openai-chat-completions]] — companion SDK pattern.
- [[chunking-strategies]] — upstream of every embed call.
- [[agentic-rag]] — downstream consumer of search results.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` chooses (a) Batch API vs synchronous based on the 24-hour latency budget, (b) text-embedding-3-small vs text-embedding-3-large by measured recall, and (c) full dims vs reduced dims by cost ceiling. Use it before the first ingestion run — switching after re-indexes the entire corpus.
