# Embedding Models

## Summary

Reference for selecting and calling API and local embedding models: OpenAI text-embedding-3, Mistral embed, Cohere embed-v3, local sentence-transformers (BGE-M3, bge-large-en-v1.5, MiniLM), and production patterns (async batch, retry with backoff, full pipeline). Model selection is a load-bearing decision: a model change invalidates the entire index.

## Why

Different models trade off quality, cost, context length, and language coverage. text-embedding-3-large leads MTEB benchmarks for English but costs 6x more than text-embedding-3-small and stores 2x more per vector. Local models (BGE-M3) are free and support multilingual + sparse output for hybrid search, but require GPU for production throughput. Cohere v3's `input_type` asymmetry (search_document vs search_query) improves retrieval NDCG by 5-10% over generic mode.

## When To Use

- Selecting an embedding model at the start of a RAG project (pin model before indexing)
- Benchmarking multiple providers to find the best price/quality ratio for a specific corpus
- Migrating an index from one model to another (e.g., ada-002 → text-embedding-3-large)
- Building code-search RAG where general-purpose models underperform (use voyage-code-3 or BGE-M3)
- Processing multilingual corpora where English-only models degrade retrieval quality

## When NOT To Use

- Corpus is already indexed and migration cost outweighs quality gain — benchmark first
- Latency budget is <20ms — API models add network RTT; local models add model-load overhead
- Fully offline/air-gapped deployment with no GPU — local models on CPU are slow for batches >1k

## Content

| File | What's inside |
|------|---------------|
| `content/01-providers.xml` | OpenAI, Mistral, Cohere, and local sentence-transformers code examples |
| `content/02-production.xml` | Async batch processing, retry with exponential backoff, full EmbeddingPipeline |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_pipeline.py` | EmbeddingConfig + EmbeddingPipeline: chunk → cache check → batch embed |
