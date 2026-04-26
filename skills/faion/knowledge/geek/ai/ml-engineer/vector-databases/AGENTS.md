# Vector Databases

## Summary

Specialized storage systems optimized for high-dimensional vector similarity search. Covers selection (Qdrant, Weaviate, Milvus, Pinecone, pgvector, Chroma), indexing strategies (HNSW, IVF, quantization), hybrid search (dense + sparse), and production configuration rules for RAG pipelines and semantic search.

## Why

Vector databases solve approximate nearest neighbor (ANN) search at scale — finding semantically similar items without exact keyword matching. The choice of database, index type, and quantization strategy determines recall accuracy, query latency, memory usage, and operational complexity. Wrong choices are expensive to migrate later.

## When To Use

- Building a RAG pipeline requiring semantic similarity search over 10K+ documents
- Storing and querying document embeddings at scale
- Multi-tenant knowledge bases with namespace isolation
- Replacing keyword-only search with semantic or hybrid search

## When NOT To Use

- Dataset fits in memory and has fewer than ~1,000 documents — use in-process numpy similarity instead
- Requirement is pure exact-match lookup — a relational DB or Redis suffices
- Application already uses Elasticsearch with kNN and a rewrite is not justified
- Prototyping a single-user tool with no persistence requirement — Chroma in-memory suffices

## Content

| File | What's inside |
|------|---------------|
| `content/01-selection.xml` | DB comparison table, selection decision tree by constraint, per-DB strengths and weaknesses |
| `content/02-indexing.xml` | HNSW/IVF parameters, quantization trade-offs, hybrid search, production configuration rules |
| `content/03-operations.xml` | Agent retrieval pattern, gotchas (embedding mismatch, score threshold, stale index), best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant-setup.py` | Qdrant collection creation with HNSW + scalar quantization + payload index |
