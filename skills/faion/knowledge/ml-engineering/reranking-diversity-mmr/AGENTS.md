# Diversity-Aware Reranking with Maximal Marginal Relevance (MMR)

## Summary

**One-sentence:** Reranks top-N candidates with MMR to balance query relevance and inter-doc diversity, returning a diverse top-K.

**One-paragraph:** Maximal Marginal Relevance (MMR) reranking selects documents that are both relevant to the query and dissimilar to already-selected documents. The lambda parameter balances relevance (λ→1) vs diversity (λ→0). MMR is the right choice when the retriever returns near-duplicate or highly redundant top-K, but it adds O(N×K) similarity comparisons on top of the base retrieval cost.

**Ефективно для:** інженерів RAG, у яких top-K насичений near-duplicate чанками й треба покрити кілька різних аспектів запиту.

## Applies If (ALL must hold)

- Top-K from retrieval is dominated by near-duplicate chunks.
- Query is broad and a diverse multi-faceted answer is expected.
- Downstream LLM context budget is tight and redundant chunks waste it.
- Embeddings for candidate chunks are available for pairwise similarity.

## Skip If (ANY kills it)

- Top-K already diverse — MMR cost is wasted.
- Single-fact factoid queries — diversity is irrelevant.
- Retriever returns < K * 2 candidates — MMR has nothing to choose from.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Candidate pool (N >= 2K) | list of {id, score, embedding} | retrieval step |
| Query embedding | vector | embedding-generation |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/reranking-two-stage` | MMR runs as the second stage. |
| `geek/ai/rag-engineer/embedding-generation` | Candidates carry embeddings. |

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
| Score candidates with MMR | haiku | Mechanical pairwise loop. |
| Tune λ on a labeled set | sonnet | Multi-criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mmr.py` | MMR algorithm with explicit λ + pool. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking-diversity-mmr.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[reranking-two-stage]]
- [[reranking-pipeline-integration]]
- [[reranking-models]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides MMR vs skip based on pool redundancy and query type. Each leaf references a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/mmr.py`

```python
import math
from typing import List, Dict


def cosine(a, b):
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def mmr(query_embedding, candidates: List[Dict], lambda_: float = 0.5, top_k: int = 5) -> Dict:
    selected: List[Dict] = []
    pool = list(candidates)
    while pool and len(selected) < top_k:
        best, best_score = None, -1e9
        for c in pool:
            rel = cosine(query_embedding, c['embedding'])
            div = max((cosine(c['embedding'], s['embedding']) for s in selected), default=0.0)
            score = lambda_ * rel - (1 - lambda_) * div
            if score > best_score:
                best, best_score = c, score
                best_rel = rel
                best_div = div
        selected.append({'id': best['id'], 'relevance': best_rel, 'diversity_penalty': best_div, 'mmr_score': best_score})
        pool.remove(best)
    return {'lambda': lambda_, 'pool_n': len(candidates), 'top_k': top_k, 'results': selected}
```
