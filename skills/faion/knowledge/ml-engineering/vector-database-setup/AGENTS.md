# Vector Database Setup

## Summary

**One-sentence:** Picks and provisions a vector DB (Pinecone/Weaviate/Chroma/Qdrant/Milvus/pgvector) with the right index (HNSW/IVF/Flat) for the RAG workload.

**One-paragraph:** Decision methodology for choosing and provisioning a vector database at the start of a RAG project: comparison of Pinecone, Weaviate, Chroma, Qdrant, Milvus, and pgvector; HNSW vs IVF vs Flat index selection; setup code for each provider; and a provider-agnostic VectorStoreBase abstraction.

**Ефективно для:** інженерів, які роблять перший вибір сховища векторів і не хочуть бути замкненими на одного вендора.

## Applies If (ALL must hold)

- Starting a new RAG project and choosing the vector DB.
- Migrating from a prototype DB (Chroma) to production DB.
- Workload characteristics (vector count, queries/sec, filtering needs) are known.
- Self-host vs managed decision is open.

## Skip If (ANY kills it)

- Existing vector DB already in production and switching is not justified.
- Vector count < 10k and prototyping — Chroma is the default; no decision needed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Expected vector count + growth rate | estimate | product |
| Queries/sec target | estimate | product |
| Filtering needs (metadata predicates) | list | product |
| Self-host vs managed policy | decision | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/embedding-models` | Dimensionality from embedding choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Bench candidate DBs | haiku | Mechanical loop. |
| Draft decision record | sonnet | Trade-off framing. |
| Novel deployment patterns | opus | Cross-vendor judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vector-store-base.py` | VectorStoreBase abstraction with cosine / dot / l2 dispatch. |
| `templates/vector-db-decision.md` | Decision record skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-database-setup.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-architecture]]
- [[embedding-models]]
- [[hybrid-search-implementation]]
- [[db-qdrant]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks vector DB + index by scale + ops policy + filter needs. Each leaf references a rule id from `01-core-rules.xml`.
