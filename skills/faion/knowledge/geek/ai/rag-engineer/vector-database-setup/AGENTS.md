---
slug: vector-database-setup
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Decision methodology for choosing and provisioning a vector database at the start of a RAG project: comparison of Pinecone, Weaviate, Chroma, Qdrant, Milvus, and pgvector; HNSW vs IVF vs Flat index selection; setup code for each provider; and a provider-agnostic VectorStoreBase abstraction.
content_id: "0c21a5740b2aff61"
tags: [vector-database, rag, embeddings, ann, pinecone, qdrant]
---
# Vector Database Setup

## Summary

**One-sentence:** Decision methodology for choosing and provisioning a vector database at the start of a RAG project: comparison of Pinecone, Weaviate, Chroma, Qdrant, Milvus, and pgvector; HNSW vs IVF vs Flat index selection; setup code for each provider; and a provider-agnostic VectorStoreBase abstraction.

**One-paragraph:** Decision methodology for choosing and provisioning a vector database at the start of a RAG project: comparison of Pinecone, Weaviate, Chroma, Qdrant, Milvus, and pgvector; HNSW vs IVF vs Flat index selection; setup code for each provider; and a provider-agnostic VectorStoreBase abstraction. Distance metric and index type must be decided before the first upsert because both are irreversible without recreating the collection.

## Applies If (ALL must hold)

- Starting a new RAG pipeline that needs a vector store
- Migrating from one vector DB to another (e.g., Chroma → Qdrant for production)
- Building multi-tenant search requiring data isolation by namespace/collection
- Embedding datasets with >10K vectors where in-memory numpy arrays are no longer viable
- Recommendation or duplicate-detection systems needing fast ANN at scale

## Skip If (ANY kills it)

- Fewer than 5K vectors with no strict latency SLA — numpy cosine search is sufficient, zero infra
- Relational data with complex JOINs — pgvector's SQL expressiveness matters more than ANN speed
- Text search where full BM25/TF-IDF ranking is primary — use Elasticsearch or Typesense instead
- Throwaway experiments with no persistence — in-memory Chroma is simpler

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/rag-engineer/`
