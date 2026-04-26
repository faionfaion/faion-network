# Embedding Generation

## Summary

Converts text chunks into dense vectors using an embedding model so they can be stored in a vector database and retrieved by semantic similarity. The indexing step takes `{id, text}` chunk dicts, batches them, and returns `{id, embedding, model, dimensions}` dicts. The query step embeds the user query with the same model and measures cosine similarity against the stored vectors.

## Why

Semantic search requires all text to live in a shared vector space where distance reflects meaning. Without consistent embedding (same model, same preprocessing), similarity scores are meaningless — querying with a different model than was used for indexing returns garbage rankings. Batching and caching are required to make the embedding step economical at scale.

## When To Use

- Building the indexing step of any RAG pipeline (chunks → vectors)
- Implementing semantic search over a document corpus
- Text clustering, deduplication by semantic similarity, or recommendation systems
- Evaluating embedding model options for a new project before committing to a provider
- Optimizing an existing embedding pipeline for cost, latency, or quality

## When NOT To Use

- Exact-string keyword search is sufficient — embeddings add cost/latency with no precision gain for exact matches
- Very short texts (<10 tokens) — BM25 outperforms semantic similarity at this scale
- Corpus is in a low-resource language without a multilingual model — embeddings may produce near-random vectors
- Storage budget is constrained and 1536-3072 dimension vectors would overflow it — benchmark with reduced dimensions first

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Model selection rules, batching rules, caching rules, normalization rules, and pitfalls |
| `content/02-providers.xml` | Code examples for OpenAI, local SentenceTransformers, Ollama, and Cohere providers |
| `content/03-production.xml` | EmbeddingService dataclass, EmbeddingCache, similarity helpers, and normalization utils |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_service.py` | Production EmbeddingService with provider dispatch, caching, and batch support |
| `templates/embedding_cache.py` | File-based EmbeddingCache keyed by hash(text + model) |
