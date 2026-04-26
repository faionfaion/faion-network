# Chroma Vector Database

## Summary

Chroma is an in-process or persistent vector store backed by SQLite/HNSW, ideal for local development and prototyping. Install with `pip install chromadb`; no external server required. Collections are created with a fixed distance metric (cosine, L2, or IP) that cannot be changed after creation. Query results return distances, not similarity scores; for cosine space convert via `similarity = 1 - distance`.

## Why

Chroma removes all infrastructure friction for RAG prototyping: one Python import, one directory, zero Docker. Its `get_or_create_collection` pattern makes ingestion re-runs idempotent. It integrates directly with LangChain and LlamaIndex, covering the common development → eval → staging path before promoting to Qdrant or Pinecone for production.

## When To Use

- Local development and prototyping of RAG pipelines (no external server needed)
- Single-developer projects or small teams where operational simplicity trumps scale
- Running evaluation harnesses in CI where spinning up Qdrant/Weaviate adds friction
- Notebook-based research and experimentation with embeddings
- Applications needing an embedded vector store with zero infrastructure (SQLite role)

## When NOT To Use

- Production deployments with >1M vectors — Chroma performance degrades and lacks Qdrant's tuning knobs
- Multi-tenant SaaS — Chroma has no native access control or tenant isolation
- High-concurrency write workloads — PersistentClient uses SQLite; concurrent writes from multiple processes corrupt the DB
- Multi-node horizontal scaling — Chroma does not support distributed deployment

## Content

| File | What's inside |
|------|---------------|
| `content/01-usage.xml` | Collection creation, upsert, query, update, delete patterns; rules for IDs and distance conversion |
| `content/02-langchain.xml` | LangChain Chroma integration: from_documents, load existing, similarity_search_with_score |

## Templates

| File | Purpose |
|------|---------|
| `templates/chroma_store.py` | Minimal ChromaStore wrapper implementing upsert, search, delete with distance-to-similarity conversion |
