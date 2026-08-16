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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-search-basics.py` | Validates a hybrid-config YAML against the schema. | Pre-commit; CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[hybrid-search-implementation]]
- [[embedding-models]]
- [[reranking-two-stage]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks fusion strategy: root question — "Are dense and sparse leg score distributions comparable across queries?" — branches lead to RRF (rank-based, default), linear alpha (when calibrated), or "skip hybrid" (when latency budget kills it). Each leaf references a rule from 01-core-rules.xml.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/hybrid-config.yaml`

```yaml
fusion: rrf            # rrf | linear
rrf_k: 60              # only when fusion=rrf
# alpha: 0.5           # only when fusion=linear (must be set then)
dense:
  index: qdrant://docs
  model: text-embedding-3-large
sparse:
  backend: bm25        # bm25 | splade | tantivy
k: 10
tie_break: dense_rank  # dense_rank | sparse_rank | doc_id
eval:
  dataset: labeled-queries-v2
  metric: ndcg@10
  score: 0.74
```

### `templates/alpha-sweep.py`

```python
from typing import Callable, List, Dict


def ndcg_at_k(ranked_ids: List[str], relevant_ids: set, k: int = 10) -> float:
    import math
    dcg = 0.0
    for i, doc_id in enumerate(ranked_ids[:k]):
        if doc_id in relevant_ids:
            dcg += 1.0 / math.log2(i + 2)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(len(relevant_ids), k)))
    return dcg / ideal if ideal > 0 else 0.0


def sweep(
    queries: List[Dict],
    dense_search: Callable[[str, int], List[Dict]],
    sparse_search: Callable[[str, int], List[Dict]],
    k_pool: int = 50,
    k_eval: int = 10,
) -> Dict[float, float]:
    results: Dict[float, float] = {}
    for alpha in (0.0, 0.25, 0.5, 0.75, 1.0):
        scores = []
        for q in queries:
            dense = {d["id"]: float(d["score"]) for d in dense_search(q["query"], k_pool)}
            sparse = {d["id"]: float(d["score"]) for d in sparse_search(q["query"], k_pool)}
            # min-max normalise per leg
            def norm(d):
                if not d:
                    return {}
                lo, hi = min(d.values()), max(d.values())
                return {k_: (v - lo) / (hi - lo + 1e-9) for k_, v in d.items()}
            d_n = norm(dense)
            s_n = norm(sparse)
            ids = set(d_n) | set(s_n)
            fused = {i: alpha * d_n.get(i, 0) + (1 - alpha) * s_n.get(i, 0) for i in ids}
            ranked = sorted(fused, key=fused.get, reverse=True)
            scores.append(ndcg_at_k(ranked, set(q["relevant_ids"]), k_eval))
        avg = sum(scores) / len(scores) if scores else 0.0
        results[alpha] = avg
        print(f"alpha={alpha:.2f}  ndcg@{k_eval}={avg:.4f}")
    return results
```

### `templates/_smoke-test.yaml`

```yaml
fusion: rrf
rrf_k: 60
dense:
  index: qdrant://docs-prod-2026Q2
  model: text-embedding-3-large
sparse:
  backend: bm25
k: 10
tie_break: dense_rank
eval:
  dataset: docs-labeled-queries-v3
  metric: ndcg@10
  score: 0.78
```
