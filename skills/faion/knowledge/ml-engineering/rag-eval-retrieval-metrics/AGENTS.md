# RAG Retrieval Quality Metrics

## Summary

**One-sentence:** Computes Precision@K, Recall@K, MRR, NDCG and hit-rate for a RAG retrieval pass and exports a per-query JSONL.

**One-paragraph:** Retrieval metrics measure whether the RAG system fetches the right documents before generation happens. The standard quartet is Precision@K, Recall@K, MRR, NDCG, plus an end-to-end hit-rate. Ground-truth labels for relevant chunks are required. These metrics are inputs to rag-eval-pipeline; on their own they isolate retrieval from generation failure modes.

**Ефективно для:** інженерів, які діагностують RAG-провали і хочуть локалізувати, чи це retrieval-fail (а не generation).

## Applies If (ALL must hold)

- Diagnosing whether a quality regression is retrieval-side or generation-side.
- Tuning chunk size, embedding model, or reranker with measurable retrieval signal.
- Building a baseline before adding a reranker.
- Ground-truth-labeled test set is available.

## Skip If (ANY kills it)

- No labeled relevant chunks — only generation metrics are possible.
- Only end-to-end answer quality matters — use rag-eval-pipeline directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Test set with relevant chunk ids | JSONL {query, relevant_chunk_ids[]} | rag-eval-test-set-generation |
| Retrieval runner | callable | rag-implementation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-test-set-generation` | Source of labeled relevant chunks. |

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
| Compute per-query metrics | haiku | Pure arithmetic. |
| Aggregate report | sonnet | Per-bucket analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retrieval-metrics.py` | Per-query metric functions: precision_at_k, recall_at_k, mrr, ndcg. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-retrieval-metrics.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-generation-metrics]]
- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks metric set based on label type (binary vs graded vs missing). Each leaf references a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/retrieval-metrics.py`

```python
import math
from typing import List, Dict, Optional


def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if k <= 0:
        return 0.0
    return sum(1 for x in retrieved[:k] if x in set(relevant)) / k


def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if not relevant:
        return 0.0
    return sum(1 for x in retrieved[:k] if x in set(relevant)) / len(relevant)


def mrr(retrieved: List[str], relevant: List[str]) -> float:
    s = set(relevant)
    for i, x in enumerate(retrieved, 1):
        if x in s:
            return 1.0 / i
    return 0.0


def ndcg_at_k(retrieved: List[str], graded: Dict[str, float], k: int) -> float:
    dcg = 0.0
    for i, x in enumerate(retrieved[:k]):
        rel = graded.get(x, 0.0)
        dcg += (2 ** rel - 1) / math.log2(i + 2)
    ideal = sorted(graded.values(), reverse=True)[:k]
    idcg = sum((2 ** r - 1) / math.log2(i + 2) for i, r in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0
```
