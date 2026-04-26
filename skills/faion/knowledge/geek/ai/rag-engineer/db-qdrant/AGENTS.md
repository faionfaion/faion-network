# Qdrant Vector Database

## Summary

Qdrant is the recommended production self-hosted vector database: HNSW indexing, payload-level filtering, scalar/binary quantization (4x–32x memory reduction), named multi-vector collections, native hybrid dense+sparse search via prefetch + RRF fusion, and snapshot-based backups. Run via Docker on port 6333 (REST) and 6334 (gRPC). `pip install qdrant-client`.

## Why

Qdrant outperforms Pinecone at production scale for self-hosted workloads (41 QPS @ 50M vectors) and exposes HNSW tuning knobs unavailable in Chroma. Scalar quantization halves RAM without measurable recall loss for most corpora; binary quantization achieves 32x reduction for high-dimensional models. Built-in sparse-vector support eliminates the need for a separate keyword search engine in hybrid pipelines.

## When To Use

- Standing up a production self-hosted vector store (Docker or Kubernetes)
- RAG pipelines needing payload-level filtering alongside vector similarity
- Systems requiring hybrid dense+sparse (BM25) search without a separate engine
- High-volume indexing (>1M vectors) with memory constraints
- Multi-modal retrieval (one point stores text + image vectors as named vectors)
- Pipelines requiring point-level snapshots and incremental backups

## When NOT To Use

- Prototype/local dev with <50K vectors and no filtering needs — Chroma is simpler and zero-config
- Existing PostgreSQL stack where pgvector extension is already present
- Teams that need a fully managed SaaS with zero infra ops — use Qdrant Cloud or Pinecone
- Requirements for GraphQL or Weaviate-style schema-first data modeling

## Content

| File | What's inside |
|------|---------------|
| `content/01-collection-setup.xml` | Collection creation, named vectors, HNSW config, payload indexing |
| `content/02-upsert-search.xml` | Batch upsert, filtered search, hybrid search with RRF fusion |
| `content/03-quantization.xml` | Scalar and binary quantization config and search with rescoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant_store.py` | QdrantStore wrapper: create collection, batch upsert, filtered search, snapshot |
