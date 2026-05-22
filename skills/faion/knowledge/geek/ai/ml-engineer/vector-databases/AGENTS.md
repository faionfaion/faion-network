---
slug: vector-databases
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "14759711afc1940a"
summary: Picks a vector database (Qdrant, Weaviate, Milvus, pgvector, Pinecone, Chroma) by operational profile (managed vs self-host, scale, filtering, hybrid search) and ships the connection + collection spec.
complexity: medium
produces: spec
est_tokens: 3600
tags: [vector-databases, rag, semantic-search, embeddings, similarity-search]
---

# Vector Databases

## Summary

**One-sentence:** Selects a vector DB across Qdrant (self-host fast filtered), pgvector (Postgres exists), Pinecone (managed serverless), Weaviate (graphs + hybrid), Milvus (billions-scale), or Chroma (dev only) using a decision tree driven by scale + filtering + ops profile.

**One-paragraph:** Vector DB choice spans operational complexity, cost, and capability. 2026 benchmarks: Qdrant p99 latency at 10M vectors ≈12ms, Weaviate ≈16ms, Milvus ≈18ms. Qdrant leads filtered search ("find similar AND in_stock AND under $50"); pgvector wins when Postgres already exists; Pinecone removes ops burden at managed cost; Milvus is the only one routinely deployed at 100M-1B vectors. Output: a `vector-db.yaml` declaring connection, collection schema, embedding dim, metric (cosine / dot / euclidean), hybrid-search wiring (vector + BM25 fused via RRF), and multi-tenant filter rule.

**Ефективно для:**

- Self-host RAG де треба filtering — Qdrant найшвидший на complex metadata filters.
- Команд з Postgres — pgvector економить інфра без нового сервісу (до 2K dim, &lt;10M vectors).
- Multi-tenant SaaS — Qdrant payload filter або Pinecone namespaces.
- Billion-scale catalog — Milvus з disaggregated архітектурою.

## Applies If (ALL must hold)

- Need to do similarity search over embeddings at scale (corpus &gt; 1k vectors)
- Filtering by metadata required OR semantic dedup OR hybrid search
- Acceptable to maintain a vector store (self-host OR pay managed)

## Skip If (ANY kills it)

- Corpus &lt;1k vectors — keep them in memory, search with numpy
- Need full-text search only — use Elastic / Typesense / Postgres GIN, not vector DB
- Embeddings will change daily — fix the embedding choice first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `corpus-profile.yaml` | YAML | vector count, dim, metadata schema, growth rate |
| `ops-constraints.yaml` | YAML | managed vs self-host, GPU access, Kubernetes vs VM |
| `multi-tenant-plan.yaml` | YAML | tenant isolation strategy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `rag-pipeline-design` | DB picked as part of pipeline tier |
| `vector-db-setup-dev` | Dev-mode setup |
| `vector-db-setup-prod` | Prod-mode setup |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pick by profile, pin embedding model, tenant filter required, hybrid as default, metric matches embedding | 1100 |
| `content/02-output-contract.xml` | essential | vector-db.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: Chroma in prod, missing tenant filter, dim mismatch, wrong metric, no backup | 900 |
| `content/04-procedure.xml` | essential | 5 steps: profile → pick → ingest plan → tenant policy → ship | 700 |
| `content/05-examples.xml` | essential | Worked example: 10M-vector Qdrant on-prem with payload filter | 500 |
| `content/06-decision-tree.xml` | essential | Routes by scale + filtering + ops to a specific DB | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `db_selection_drafting` | sonnet | Trade-off analysis |
| `corpus_profile_extraction` | haiku | Counting / sum / aggregation |
| `vector_db_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant-setup.py` | Qdrant collection create + ingest skeleton |
| `templates/vector-db.schema.yaml` | Schema for vector-db.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable vector-db spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-databases.py` | Lint vector-db.yaml | Pre-commit |

## Related

- [[rag-pipeline-design]] · [[vector-db-setup-dev]] · [[vector-db-setup-prod]] · [[vector-db-index-tuning]] · [[vector-db-monitoring]] · [[vector-db-security]]
- external: [Qdrant docs](https://qdrant.tech/documentation/) · [pgvector](https://github.com/pgvector/pgvector) · [Pinecone](https://www.pinecone.io/learn/)

## Decision tree

See `content/06-decision-tree.xml`. Routes by (a) Postgres-exists, (b) scale tier (1M/100M/1B), (c) managed-vs-self-host, (d) hybrid search need → {Qdrant, pgvector, Pinecone, Weaviate, Milvus, Chroma}.
