# Reranking Pipeline Integration for RAG

## Summary

**One-sentence:** Wraps two-stage retrieve + rerank in a RerankingRAG class supporting cross-encoder, Cohere, and LLM rerankers behind one interface.

**One-paragraph:** Integrate reranking into a production RAG pipeline by wrapping the two-stage retrieve + rerank flow in a RerankingRAG class, supporting cross-encoder, Cohere API, and LLM-based rerankers behind a uniform interface with a circuit breaker, warmup, and graceful fallback to ANN top-K on rerank failure.

**Ефективно для:** інженерів, які доводять reranking-models вибір до боєвого pipeline-сервісу з warmup, circuit-breaker і fallback.

## Applies If (ALL must hold)

- Two-stage RAG retrieval is the chosen architecture.
- Multiple reranker backends must be swappable behind one interface.
- Pipeline must keep working when the reranker is unavailable.
- Need consistent metrics + logging across all reranker types.

## Skip If (ANY kills it)

- Single-stage retrieval is the design.
- Only one reranker backend is ever used and no abstraction is needed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Reranker choice + config | yaml | reranking-models |
| Vector retrieval client | callable | vector-database-setup |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/reranking-models` | Decides which reranker. |
| `geek/ai/rag-engineer/reranking-two-stage` | Two-stage flow shape. |

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
| Write RerankingRAG class | sonnet | Multi-backend abstraction. |
| Wire circuit breaker | haiku | Mechanical pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reranking_rag.py.tmpl` | RerankingRAG class skeleton with backends + circuit breaker. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking-pipeline-integration.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[reranking-models]]
- [[reranking-two-stage]]
- [[rag-implementation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides class abstraction vs minimal wrap vs skip based on swap likelihood. Each leaf references a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/reranking_rag.py.tmpl`

```python
import time
from typing import Callable, List, Dict


class CircuitBreaker:
    def __init__(self, threshold=5, window_s=60, cooldown_s=30):
        self.threshold = threshold
        self.window_s = window_s
        self.cooldown_s = cooldown_s
        self.failures: List[float] = []
        self.opened_at = 0.0

    def open(self):
        now = time.time()
        if self.opened_at and now - self.opened_at < self.cooldown_s:
            return True
        self.failures = [t for t in self.failures if now - t < self.window_s]
        return len(self.failures) >= self.threshold

    def record_failure(self):
        self.failures.append(time.time())
        if len(self.failures) >= self.threshold:
            self.opened_at = time.time()


class RerankingRAG:
    def __init__(self, retriever: Callable[[str, int], List[Dict]], reranker: Callable[[str, List[Dict], int], List[Dict]], warmup: Callable[[], None] = None):
        self.retriever = retriever
        self.reranker = reranker
        self.breaker = CircuitBreaker()
        if warmup is not None:
            try:
                warmup()
            except Exception:
                pass

    def retrieve(self, query: str, top_k: int = 5, pool: int = 50) -> Dict:
        t0 = time.time()
        cands = self.retriever(query, pool)
        t1 = time.time()
        retrieval_ms = (t1 - t0) * 1000
        degraded = False
        if self.breaker.open():
            results = cands[:top_k]
            degraded = True
            rerank_ms = 0.0
        else:
            try:
                ranked = self.reranker(query, cands, top_k)
                rerank_ms = (time.time() - t1) * 1000
                results = ranked
            except Exception:
                self.breaker.record_failure()
                results = cands[:top_k]
                rerank_ms = 0.0
                degraded = True
        formatted = [{'id': r['id'], 'score': float(r.get('score', 0.0)), 'source': 'rerank' if not degraded else 'ann'} for r in results]
        return {'query': query, 'results': formatted, 'latency': {'retrieval_ms': retrieval_ms, 'rerank_ms': rerank_ms}, 'degraded': degraded}
```
