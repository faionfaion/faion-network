# Hybrid Search Basics

## Summary

Hybrid search combines dense vector search (semantic similarity) with sparse lexical search (BM25/keyword) and fuses the ranked results using Reciprocal Rank Fusion (RRF) or weighted linear combination. RRF is the default fusion strategy. The balance between semantic and keyword signals is controlled by an alpha parameter (1.0 = pure semantic, 0.0 = pure keyword) that should be tuned per domain on a labeled query set. Native hybrid is available in Qdrant, Weaviate, and Elasticsearch.

## Why

Pure semantic search misses exact technical terms, product codes, model numbers, and rare names because the embedding space blurs them. Pure keyword search misses paraphrases, synonyms, and conceptual queries. Hybrid search captures both: semantic for intent, keyword for precision. RRF is more robust than linear score normalization because it operates on rank positions rather than raw scores, which have incompatible scales between BM25 and cosine similarity.

## When To Use

- Document corpus contains exact technical terms, product codes, or names that semantic search misses.
- Domain is legal, medical, or compliance-heavy where precise phrase matching is required.
- User queries mix conceptual intent with specific identifiers.
- Pure vector search recall is below acceptable threshold on benchmark query set.
- System uses Qdrant, Weaviate, or Elasticsearch — all support hybrid natively.

## When NOT To Use

- Corpus is purely natural-language prose with no technical identifiers — pure semantic suffices.
- Latency budget is very tight (< 100ms) — hybrid adds BM25 scoring overhead.
- Corpus is too small (< 500 documents) — BM25 gains are negligible at small scale.
- Already using a cross-encoder reranker over broad vector retrieval — reranker compensates for keyword misses.

## Content

| File | What's inside |
|------|---------------|
| `content/01-fusion-strategies.xml` | RRF algorithm, linear fusion, alpha parameter rules, score normalization gotchas. |
| `content/02-implementation.xml` | Qdrant native hybrid, dynamic alpha selection, BM25 preprocessing requirements, index rebuild rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rrf-fuse.py` | Provider-agnostic RRF fusion of ranked ID lists. |
| `templates/dynamic-alpha.py` | Alpha selection logic based on query characteristics (quotes, codes, length). |
