# Weaviate Vector Database

## Summary

**One-sentence:** Vector database for knowledge-graph + native hybrid (vector + BM25) workloads via GraphQL, with multi-vector multi-modal objects, scaling 10M–100M vectors self-hosted or via Weaviate Cloud.

**One-paragraph:** Weaviate combines vector + cross-reference graph + native BM25 in one query surface — eliminating client-side fusion code for hybrid pipelines. Python client v4 is required (v3 is incompatible). Classes define schema with `vectorizer` (or `none` for client-supplied vectors), `properties`, and `cross-references`. Multi-modal objects use named vectors. Replication factor and sharding are set at schema creation.

**Ефективно для:** RAG engineer building entity-linked knowledge graphs OR pipelines needing one-call hybrid search — closes the gap between maintaining vector + BM25 + graph as separate services.

## Applies If (ALL must hold)

- Knowledge-graph relationships required (entities with cross-references).
- Native hybrid (vector + BM25) needed without client-side fusion.
- GraphQL fits the team's API tooling.
- Self-hosted (Docker / K8s) at 10M–100M vectors OR Weaviate Cloud.

## Skip If (ANY kills it)

- Simple RAG prototype, no graph — Chroma or Qdrant are simpler.
- Team unfamiliar with GraphQL — Qdrant (REST/gRPC) is friendlier.
- Payload-filter perf at very high cardinality is the binding need — Qdrant outperforms.
- Cost-sensitive 1B+ managed — Pinecone / Milvus offer better per-vector pricing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| weaviate-client | python pkg, **v4+** | `pip install weaviate-client` |
| Weaviate instance | URL + API key | Docker or Weaviate Cloud (WCS) |
| Schema definition | classes + properties + cross-refs | domain modelling |
| Vectorizer choice | `text2vec-openai` / `none` / `multi2vec-clip` | per use case |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/db-comparison` | Why Weaviate over Qdrant. |
| `geek/ai/rag-engineer/hybrid-search-implementation` | Hybrid scoring semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: v4 client, schema-first, native hybrid not client fusion, replication factor at schema, multi-vector for multi-modal | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for hybrid search response with alpha + sub-scores | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: v3 client mixed, manual fusion, no replication, missing cross-refs | ~700 |
| `content/04-procedure.xml` | deep | 6 steps: bring up → schema → cross-refs → upsert → hybrid query → backup | ~700 |
| `content/06-decision-tree.xml` | essential | Routes graph + hybrid + scale | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-design` | sonnet | Domain modelling judgement. |
| `hybrid-tune-alpha` | sonnet | Recall/precision tradeoff with benchmarks. |
| `bulk-import` | haiku | I/O. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weaviate_store.py` | WeaviateStore wrapper using client v4 with hybrid + cross-ref helpers. |
| `templates/weaviate-schema.json` | JSON Schema for search response. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-db-weaviate.py` | Verify hybrid response carries alpha + sub-scores; flag manual fusion smell. | Post-query, pre-commit. |

## Related

- [[db-qdrant]] · [[db-comparison]] · [[hybrid-search-implementation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by knowledge-graph need, hybrid-search need, scale, and team GraphQL familiarity to Weaviate or an alternative.
