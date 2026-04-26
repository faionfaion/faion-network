# Hybrid Search for RAG

## Summary

Hybrid search combines BM25 (sparse/keyword) and vector (dense/semantic) retrieval to maximize precision and recall. Use Reciprocal Rank Fusion (RRF) as the default fusion method — it requires no score normalization and works across different score scales. Add a cross-encoder reranker (Cohere, bge-reranker-v2-m3) only if precision is still insufficient after hybrid. Benchmarks: hybrid + reranking achieves 87% relevant docs in top-10 vs 62% BM25-only and 71% vector-only.

## Why

BM25 excels at exact term matching (product codes, error messages, names); vector search excels at semantic similarity (synonyms, paraphrases, intent). Neither alone handles queries that combine both — enterprise search, technical docs, legal/compliance. Hybrid captures the complementary strengths, with only ~20% latency overhead.

## When To Use

- RAG pipeline serves queries mixing natural language and exact terms (product codes, error messages, statute numbers)
- Pure vector search precision is inadequate (&lt;75% relevant in top-10) and queries include specific keywords
- Enterprise search over technical documentation with alternating concept searches and exact string lookups
- Production system where +15% precision gain justifies ~20% additional latency and complexity
- Replacing existing BM25-only search with semantic capability

## When NOT To Use

- Corpus is &lt;1,000 documents — pure vector is simpler and fast enough
- All queries are conversational/semantic with no exact term requirements
- Latency budget is under 20ms — hybrid (parallel BM25 + vector + fusion) costs 40-100ms
- Infrastructure is Elasticsearch-only — native kNN + BM25 in ES is effective without adding a second vector DB

## Content

| File | What's inside |
|------|---------------|
| `content/01-fusion-methods.xml` | RRF vs linear combination, query-adaptive alpha, reranking, vector DB comparison |
| `content/02-rules.xml` | Concrete rules, score normalization, BM25 parameters, failure modes, production gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/rrf.py` | Reciprocal Rank Fusion implementation |
| `templates/qdrant-hybrid.py` | Qdrant native hybrid search with FusionQuery |
