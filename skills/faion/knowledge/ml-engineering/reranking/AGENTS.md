# Reranking for RAG Systems

## Summary

**One-sentence:** Two-stage retrieval — fast bi-encoder for top-N candidates + slow cross-encoder reranker for top-K — that lifts RAG accuracy 20-35% while adding 100-500ms latency per query.

**One-paragraph:** First-stage retrieval (bi-encoder or hybrid) prioritises recall and speed but compresses query+doc into independent vectors, losing nuanced relevance signals. Cross-encoder rerankers (Cohere Rerank, BGE Reranker, FlashRank, Voyage Rerank) jointly encode query+doc pairs with full attention, recovering precision. The pattern: retrieve top-N (20-100) with vector / hybrid search, rerank to top-K (3-5), pass to synthesis. Choose provider by latency / cost / privacy: Cohere managed, BGE local, FlashRank for batch. Output: a `reranker.yaml` block plugged into the parent rag-pipeline.yaml with provider + top_n + budget guardrail.

**Ефективно для:**

- Legal / medical / enterprise RAG де precision коштує грошей — reranker ловить "майже правильні" доки які перший stage пропускає.
- Hybrid search pipelines — score-fusion (vector + BM25) дає змішані score, cross-encoder нормалізує і ставить релевантний на 1-2.
- Code search — token-level relevance критичний; cross-encoder бачить що patch до function f(), а не до f2().
- Cost-sensitive але quality-критичних use case — local BGE дає 80% якості Cohere без API cost.

## Applies If (ALL must hold)

- RAG pipeline tier ≥ Advanced (rules from `rag-pipeline-design`)
- Latency budget allows ≥150ms per query for reranker call
- Retrieval recall@20 is already ≥80% (reranker improves precision, not recall)
- Queries are diverse enough that cross-encoder reordering matters (eval proves +10% precision lift)

## Skip If (ANY kills it)

- Real-time autocomplete / typeahead — &lt;50ms budget, no room for reranker
- Fewer than 10 candidates retrieved — limited reordering room; gain marginal
- First-stage recall already saturated near 100% on labelled set
- Cost-prohibitive: managed reranker exceeds budget AND no GPU for local model

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `eval-rerank.jsonl` | JSONL `{query, candidate_ids, relevance_labels}` | SME + log analysis |
| `latency-budget.yaml` | YAML | product SLO |
| `rate-cards.yaml` | YAML | Cohere / Voyage / Jina pricing |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `rag-pipeline-design` | Parent pipeline this reranker plugs into |
| `vector-databases` | First-stage retrieval comes from here |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: reranker after retrieval, top-N capacity, latency budget, eval gate, fallback on provider down | 1000 |
| `content/02-output-contract.xml` | essential | `reranker.yaml` schema (provider + top_n + budget + fallback) | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skip reranker, oversize top-N, no eval before adopt, hard-coded provider, no latency budget | 900 |
| `content/04-procedure.xml` | essential | 5 steps: measure recall → pick provider → tune top-N+top-K → wire fallback → eval+ship | 700 |
| `content/05-examples.xml` | essential | Worked example: Qdrant top-20 → Cohere Rerank top-5 with FlashRank fallback | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency budget + privacy → Cohere / Voyage / BGE / FlashRank | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `provider_selection` | sonnet | Cross-attribute comparison |
| `eval_lift_measurement` | sonnet | Run paired retrieval+rerank evaluation |
| `reranker_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/rerank-pipeline.py` | Top-N → reranker → top-K skeleton with provider abstraction |
| `templates/reranker.schema.yaml` | Schema for reranker.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable reranker spec |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking.py` | Lint reranker.yaml | Pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-pipeline-design]] — parent pipeline
- [[vector-databases]] — first-stage retrieval
- external: [Cohere Rerank](https://docs.cohere.com/docs/rerank-2) · [BGE Reranker](https://github.com/FlagOpen/FlagEmbedding) · [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank)

## Decision tree

See `content/06-decision-tree.xml`. Routes by latency budget + privacy requirement + cost cap to {Cohere Rerank, Voyage Rerank, BGE local, FlashRank batch}.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rerank-pipeline.py`

```python
"""Two-stage rerank: retrieve top-N first-stage candidates, rerank to top-K."""
from __future__ import annotations

import os
from typing import Callable

import cohere


class RerankProviderError(RuntimeError):
    pass


def cohere_rerank(query: str, candidates: list[dict], top_k: int, model: str) -> list[dict]:
    client = cohere.Client(api_key=os.environ["COHERE_API_KEY"])
    docs = [c["content"] for c in candidates]
    response = client.rerank(
        model=model,
        query=query,
        documents=docs,
        top_n=top_k,
    )
    return [
        {**candidates[r.index], "rerank_score": r.relevance_score}
        for r in response.results
    ]


def bge_local_rerank(query: str, candidates: list[dict], top_k: int, model: str) -> list[dict]:
    from sentence_transformers import CrossEncoder
    ce = CrossEncoder(model)
    pairs = [(query, c["content"]) for c in candidates]
    scores = ce.predict(pairs)
    ranked = sorted(
        ({"score": s, **c} for s, c in zip(scores, candidates)),
        key=lambda x: -x["score"],
    )[:top_k]
    return ranked


def rerank_with_fallback(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    primary: Callable = cohere_rerank,
    primary_kwargs: dict | None = None,
    fallback: Callable = bge_local_rerank,
    fallback_kwargs: dict | None = None,
) -> tuple[list[dict], bool]:
    """Return (top-k reranked, degraded_flag)."""
    primary_kwargs = primary_kwargs or {"model": "rerank-multilingual-v3.0"}
    fallback_kwargs = fallback_kwargs or {"model": "BAAI/bge-reranker-base"}
    try:
        return primary(query, candidates, top_k, **primary_kwargs), False
    except Exception:  # noqa: BLE001
        return fallback(query, candidates, top_k, **fallback_kwargs), True
```

### `templates/reranker.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, model, top_n_input, top_k_output, latency_budget_ms, fallback, eval_evidence]
properties:
  provider: { type: string, enum: [cohere, voyage, jina, bge, flashrank, none] }
  model: { type: string, minLength: 3 }
  top_n_input: { type: integer, minimum: 10, maximum: 1000 }
  top_k_output: { type: integer, minimum: 1, maximum: 20 }
  latency_budget_ms: { type: integer, minimum: 50, maximum: 2000 }
  fallback:
    type: object
    required: [strategy]
    properties:
      strategy: { type: string, enum: [local-bge, return-first-stage-degraded, hard-fail] }
      model: { type: string }
  eval_evidence:
    type: object
    required: [set_path, sample_size, precision_lift]
    properties:
      sample_size: { type: integer, minimum: 50 }
      precision_lift: { type: number, minimum: 0 }
```

### `templates/_smoke-test.yaml`

```yaml
provider: cohere
model: rerank-multilingual-v3.0
top_n_input: 20
top_k_output: 5
latency_budget_ms: 350
fallback:
  strategy: local-bge
  model: BAAI/bge-reranker-base
eval_evidence:
  set_path: evals/rerank-support-kb.jsonl
  sample_size: 84
  precision_lift: 0.21
```
