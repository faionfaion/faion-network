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
