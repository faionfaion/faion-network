---
slug: embedding-generation
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an embedding-generation config (model id, dimension, normalization, batch policy, cache layer) plus producer code for semantic-search / RAG indexing pipelines.
content_id: "3f03de6e6807daf3"
complexity: medium
produces: code
est_tokens: 3500
tags: [embeddings, vectors, rag, semantic-search, indexing]
---
# Embedding Generation

## Summary

**One-sentence:** Produces the embedding-producer config + code (model id, dimension, normalization, batch size, cache layer, retry policy) for a semantic-search / RAG / clustering pipeline.

**One-paragraph:** Embeddings are dense vector representations of text that power semantic search, RAG, clustering, classification, recommendations, and anomaly detection. This methodology covers the producer side only: choose a model whose quality, latency, dimension, and pricing match the workload (delegated to embeddings-model-selection); set up async batching for throughput; cache by content hash to deduplicate; normalize vectors so cosine similarity is dot product; persist to the vector store via a stable schema. The output is a producer config (JSON) + a Python module that emits embeddings deterministically given the same inputs.

**Ефективно для:**

- Будь-якого RAG-пайплайну, де треба перетворити тексти на вектори перед index/upsert.
- Семантичного пошуку поверх документів, тікетів, повідомлень — коли BM25 не вистачає для синонімів / парафразу.
- Кластеризації або topic-modeling: embeddings + HDBSCAN дешевше і часто кращі за LDA.
- Recommender-систем на content-based фільтрі (товари, статті).
- Anomaly-detection у текстових логах (виявлення outliers по cosine-відстані до centroid).

## Applies If (ALL must hold)

- A downstream system (vector DB, KNN index, classifier) needs vector input.
- Source text is available and can be deterministically partitioned (chunked) or used whole.
- A target vector store is chosen OR will be chosen in this iteration (Qdrant, pgvector, Pinecone, Weaviate, Chroma).

## Skip If (ANY kills it)

- Use case is structured/tabular search where BM25 + filters already match user intent — embeddings add cost without recall gain.
- Pipeline is one-off enrichment on &lt;100 documents — running embeddings via a hosted API once is cheaper than building a producer.
- Privacy / sovereignty rules forbid sending text to a hosted embedding API AND no local embedding model is approved — defer to security review first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source text corpus | strings / files | Product data layer |
| Chunking spec (size, overlap) | YAML | `chunking-strategies` methodology output |
| Selected embedding model | model id + dim | `embeddings-model-selection` output |
| Target vector store handle | client / URL | Infra |
| API key for hosted provider (if applicable) | env var | Secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[embeddings-model-selection]] | Decides which model+dimension the producer must use. |
| [[chunking-strategies]] | Decides the input shape (size, overlap) passed to the producer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: deterministic producer, content-hash cache, async batching, L2-normalize, dimension-locked schema, exponential-backoff retry | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the producer-config artefact: model_id, dim, normalize, batch_size, cache_backend, retry policy | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: dimension drift, non-deterministic chunking, unnormalized cosine, cache by raw text instead of hash | 700 |
| `content/04-procedure.xml` | reference | 5-step build: scope → cache → batch → normalize → persist | 600 |
| `content/06-decision-tree.xml` | essential | Cache + batch + normalization decision tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_chunking_spec` | haiku-4-5 | Deterministic parsing. |
| `generate_producer_code` | sonnet-4-6 | Standard code generation. |
| `audit_existing_producer` | sonnet-4-6 | Code review against rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/producer.py` | Async batched producer skeleton with content-hash cache + retry. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-generation.py` | Validate a producer-config JSON against the contract. | Pre-commit; CI gate before deploy. |

## Related

- [[embeddings-model-selection]] — chooses the model the producer wraps.
- [[embeddings-provider-apis]] — per-provider SDK quirks.
- [[embeddings-batch-and-cache]] — deep dive on batching + caching primitives.

## Decision tree

See `content/06-decision-tree.xml`. Branches on whether the corpus is large enough (≥1k docs → async batching), whether re-runs are common (yes → content-hash cache; no → no cache), and whether downstream uses cosine (yes → L2 normalize). Leaves emit a producer config shape: `cached-async-batched`, `cached-sync`, `noncached-batched`, or `noncached-sync`, each citing a rule id in `01-core-rules.xml`.
