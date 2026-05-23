# Qdrant Vector Database

## Summary

**One-sentence:** Self-hosted vector store for production RAG (41 QPS at 50M vectors), with payload-filter perf, quantization, and built-in sparse vectors for hybrid search without a separate engine.

**One-paragraph:** Qdrant runs as a single process (Docker / K8s); collections set `Distance` + HNSW config at creation. Scalar quantization halves RAM with negligible recall loss; binary quantization gives ~32x for high-dim embeddings. Built-in sparse vectors eliminate the BM25 sidecar in hybrid pipelines. Payload indexes accelerate `Filter` clauses to sub-millisecond at high cardinality. Snapshots are point-level and incremental.

**Ефективно для:** RAG engineer running self-hosted production RAG (1M+ vectors, hybrid search, payload filters) — closes the gap between Chroma's prototype-only ceiling and managed-only vendor lock-in.

## Applies If (ALL must hold)

- Production deployment, 1M+ vectors, self-hosted (Docker / K8s) or Qdrant Cloud.
- Payload filtering required alongside vector similarity.
- Hybrid (dense + sparse) search needed without a separate keyword engine.
- Snapshots / incremental backups required by the operations policy.

## Skip If (ANY kills it)

- Local prototype with <50k vectors — Chroma is simpler.
- Existing Postgres footprint with idle ops capacity — pgvector reuses infra.
- Need for fully managed SaaS without any infra ops — Qdrant Cloud or Pinecone.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| qdrant-client | python pkg | `pip install qdrant-client` |
| Qdrant instance | URL + API key | self-hosted or Qdrant Cloud |
| Collection config | Distance + HNSW m / ef_construct | tuned per corpus |
| Quantization plan | scalar / binary / none | RAM target |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/db-comparison` | Why Qdrant over alternatives. |
| `geek/ai/rag-engineer/embedding-generation` | Embedding semantics for upsert. |
| `geek/ai/rag-engineer/hybrid-search-implementation` | Sparse-vector pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: distance + HNSW at creation, payload indexes for filters, quantization tradeoffs, snapshot before schema change, named vectors for multi-modal | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for QdrantStore search response + upsert ack | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: missing payload index, mixed quantization, in-memory mode in prod, no snapshot before reindex | ~700 |
| `content/04-procedure.xml` | deep | 6 steps: install → collection create → payload indexes → upsert → quantize → snapshot | ~700 |
| `content/06-decision-tree.xml` | essential | Routes scale + hybrid + RAM budget | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bootstrap` | haiku | Mechanical collection creation. |
| `tune-hnsw` | sonnet | Iterative benchmarking + judgement. |
| `quantization-decision` | sonnet | Recall vs RAM tradeoff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant_store.py` | QdrantStore wrapper with collection bootstrap, batch upsert, filter, snapshot helpers. |
| `templates/qdrant-schema.json` | JSON Schema for QdrantStore search/upsert payloads. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-qdrant.py` | Verify search response schema; check payload index present per filter field; check snapshot before schema migration. | Pre-deploy + after each schema change. |

## Related

- [[db-chroma]] · [[db-weaviate]] · [[db-comparison]] · [[hybrid-search-implementation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by year-1 vectors, hybrid-search need, RAM budget, and ops capacity to Qdrant configuration (self-hosted vs Qdrant Cloud) with quantization choice.
