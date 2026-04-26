# OpenAI Embeddings

## Summary

Generate dense vector representations of text using OpenAI embedding models and search them with cosine similarity. Two-phase workflow: (1) ingestion — chunk documents, embed in batch, upsert into vector store; (2) query — embed user query on demand, nearest-neighbor search, return top-k chunks. Use the Batch API for nightly re-indexing (50% cost reduction).

## Why

Semantic search finds intent-matching documents that keyword search misses. Embeddings enable RAG retrieval, deduplication, clustering, and zero-shot classification without fine-tuning. The Batch API makes offline enrichment of large datasets economically viable.

## When To Use

- Semantic search over a corpus (docs, tickets, FAQs) where keyword search misses intent
- Building or extending a RAG pipeline requiring dense vector retrieval
- Deduplication or clustering of text records at scale
- Classifying user input without a fine-tuned model
- Offline/async enrichment of large datasets (Batch API for 50% cost reduction)

## When NOT To Use

- Real-time latency-sensitive paths where BM25 keyword index is fast enough
- Corpus fits in context — send documents directly to the LLM instead
- Exact string match is the requirement — embeddings are approximate
- Very short strings (1–3 words) — cosine similarity degrades; use BM25 or hybrid search

## Content

| File | What's inside |
|------|---------------|
| `content/01-embeddings.xml` | Model selection, dimensionality reduction, cosine similarity, chunking rules |
| `content/02-batch-api.xml` | Batch API workflow, custom_id ordering rule, result retrieval, pricing |

## Templates

| File | Purpose |
|------|---------|
| `templates/embed-and-search.py` | embed() + cosine() + top_k() utility functions |
