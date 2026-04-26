# Vector Database Setup

## Summary

Decision methodology for choosing and provisioning a vector database at the start of a RAG project: comparison of Pinecone, Weaviate, Chroma, Qdrant, Milvus, and pgvector; HNSW vs IVF vs Flat index selection; setup code for each provider; and a provider-agnostic VectorStoreBase abstraction. Distance metric and index type must be decided before the first upsert because both are irreversible without recreating the collection.

## Why

A wrong backend choice (Chroma for 10M vectors, wrong distance metric, no payload indexing) surfaces only at scale and requires a full re-index to fix. Selecting the right combination of hosting model, index type, and metadata strategy up-front avoids multi-day migrations. The VectorStoreBase abstraction keeps application code decoupled from the backend so future migrations require only swapping the implementation.

## When To Use

- Starting a new RAG pipeline that needs a vector store
- Migrating from one vector DB to another (e.g., Chroma → Qdrant for production)
- Building multi-tenant search requiring data isolation by namespace/collection
- Embedding datasets with >10K vectors where in-memory numpy arrays are no longer viable
- Recommendation or duplicate-detection systems needing fast ANN at scale

## When NOT To Use

- Fewer than 5K vectors with no strict latency SLA — numpy cosine search is sufficient, zero infra
- Relational data with complex JOINs — pgvector's SQL expressiveness matters more than ANN speed
- Text search where full BM25/TF-IDF ranking is primary — use Elasticsearch or Typesense instead
- Throwaway experiments with no persistence — in-memory Chroma is simpler

## Content

| File | What's inside |
|------|---------------|
| `content/01-selection.xml` | Provider comparison table, index type selection rules, pitfalls |
| `content/02-setup-examples.xml` | Setup code for Pinecone, Chroma, Qdrant, Weaviate, and pgvector |

## Templates

| File | Purpose |
|------|---------|
| `templates/vector_store_base.py` | VectorStoreBase ABC + PineconeStore + ChromaStore + VectorStoreFactory |
