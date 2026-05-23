# Hybrid Search Basics

## Summary

**One-sentence:** Produces a tuned hybrid-search config (dense + BM25 + RRF or alpha fusion) for a specific corpus with a recommended alpha and rationale.

**One-paragraph:** Hybrid search combines dense vector search (semantic similarity) with sparse lexical search (BM25/keyword) and fuses the ranked results using Reciprocal Rank Fusion (RRF) or weighted linear combination. RRF is the default fusion strategy because it operates on rank positions rather than incommensurable raw scores. The balance between semantic and keyword signals is controlled by an alpha parameter (1.0 = pure semantic, 0.0 = pure keyword) that should be tuned per domain on a labeled query set.

**Ефективно для:** інженерів RAG, у яких є технічні терміни/коди/іменовані сутності, де чистий semantic пропускає точні збіги, а чистий BM25 пропускає синоніми.

## Applies If (ALL must hold)

- Document corpus contains exact technical terms, product codes, or names that semantic search misses.
- Domain is legal, medical, or compliance-heavy where precise phrase matching is required.
- User queries mix conceptual intent with specific identifiers.
- Pure vector search recall is below acceptable threshold on the benchmark query set.

## Skip If (ANY kills it)

- Corpus is purely natural-language prose with no technical identifiers — pure semantic suffices.
- Latency budget is very tight (&lt;100ms) — hybrid adds BM25 scoring overhead.
- Index lives in a store that does not support hybrid natively and engineering time is fixed.
- The team has no labeled query set to tune alpha.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Document corpus | text + chunks | ingestion pipeline |
| Dense embeddings index | Qdrant/Weaviate/ES | embedding-generation |
| BM25 index or capability | inverted index | vector DB or ES |
| Labeled query set | JSONL {query, relevant_ids} | rag-eval-test-set-generation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/embedding-models` | Dense leg uses these models. |
| `geek/ai/rag-engineer/vector-database-setup` | The hybrid feature depends on the chosen store. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: RRF default, tune alpha, never combine raw scores, log per-leg ranks, fall back on tie | ~800 |
| `content/02-output-contract.xml` | essential | JSON config schema {alpha, fusion, dense_index, sparse_index, k} + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: raw-score sum, single-alpha-everywhere, no-eval-tuning | ~700 |
| `content/04-procedure.xml` | medium | 5-step: choose-fusion → tune-alpha → run-eval → freeze-config → log | ~700 |
| `content/06-decision-tree.xml` | essential | Tree picking RRF vs linear vs pure-vector | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Sweep alpha values on labeled set | haiku | Deterministic scoring loop. |
| Pick winner with rationale | sonnet | Weighs NDCG vs latency. |
| Report write-up | sonnet | One-page config record. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid-config.yaml` | Hybrid retrieval config skeleton (alpha, fusion, leg configs). |
| `templates/alpha-sweep.py` | Loop that runs alpha ∈ {0,0.25,0.5,0.75,1.0} and prints NDCG@10. |
| `templates/_smoke-test.yaml` | Filled example for technical-docs RAG. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-search-basics.py` | Validates a hybrid-config YAML against the schema. | Pre-commit; CI. |

## Related

- [[hybrid-search-implementation]]
- [[embedding-models]]
- [[reranking-two-stage]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks fusion strategy: root question — "Are dense and sparse leg score distributions comparable across queries?" — branches lead to RRF (rank-based, default), linear alpha (when calibrated), or "skip hybrid" (when latency budget kills it). Each leaf references a rule from 01-core-rules.xml.
