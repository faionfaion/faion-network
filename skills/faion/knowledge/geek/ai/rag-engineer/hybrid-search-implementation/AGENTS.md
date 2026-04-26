# Hybrid Search Implementation

## Summary

Combines dense vector retrieval (semantic similarity) with sparse BM25 keyword retrieval, then fuses results using Reciprocal Rank Fusion (RRF) or linear alpha-weighted combination. Covered implementations: Weaviate built-in hybrid, Qdrant prefetch+FusionQuery, Pinecone sparse-dense, Elasticsearch script_score, and a backend-agnostic HybridSearchService with dynamic alpha selection.

## Why

Pure dense retrieval underperforms on short queries, exact identifiers (function names, error codes), and queries where term frequency signals matter. BM25 is complementary: it excels at exact-match but misses semantic synonyms. Hybrid search achieves higher NDCG than either method alone across most benchmark corpora, particularly for technical and domain-specific content.

## When To Use

- RAG over technical documentation where exact identifiers matter alongside semantic meaning
- Legal, medical, or compliance corpora where specific terminology must match exactly
- Short queries (1-3 words) where semantic vectors alone underperform BM25
- Multilingual corpora where query and document languages may differ
- Upgrading a keyword-only search system to add semantic understanding without full replacement

## When NOT To Use

- Purely conversational or conceptual queries with no exact-match requirements — dense-only is simpler
- Very small corpora (<5K documents) where BM25 overhead is not justified
- Real-time indexing of streaming documents where BM25 corpus statistics must be constantly rebuilt
- Latency-critical paths where running two retrieval pipelines doubles P99 latency beyond SLA

## Content

| File | What's inside |
|------|---------------|
| `content/01-implementations.xml` | Weaviate, Qdrant, Pinecone, and Elasticsearch hybrid search code |
| `content/02-fusion-rules.xml` | RRF vs linear fusion rules, alpha selection, and pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid_search_service.py` | Backend-agnostic HybridSearchService with RRF + linear fusion and dynamic alpha |
