# Reranking Models

## Summary

**One-sentence:** Picks a reranker (cross-encoder vs Cohere/MixedBread API) for two-stage retrieval based on latency, cost, and self-host constraints.

**One-paragraph:** Two-stage retrieval: fast ANN retrieves top-50 candidates, then a reranker (cross-encoder or API service) rescores them to return top-5 for generation. Choice between local cross-encoders (ms-marco-MiniLM, bge-reranker) and API services (Cohere rerank-3, MixedBread) is driven by latency budget, cost, accuracy targets, and self-host requirements.

**Ефективно для:** інженерів, які обирають конкретну реранкер-модель для two-stage RAG: cross-encoder локально vs Cohere/MixedBread API.

## Applies If (ALL must hold)

- Two-stage RAG retrieval already designed; need to pick the actual reranker model.
- Have constraints on cost-per-query, latency p95, or self-hosting.
- Need to benchmark candidate rerankers on a labeled set.

## Skip If (ANY kills it)

- Single-stage retrieval is enough (recall target met without rerank).
- All-in on a managed retrieval product that includes reranking — pick rules don't matter.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Candidate top-N from ANN | list | rag pipeline |
| Labeled eval set | JSONL | rag-eval-test-set-generation |
| Latency + cost budgets | config | product |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/reranking-two-stage` | Two-stage pattern this model plugs into. |

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
| Run rerank benchmarks | haiku | Mechanical eval loop. |
| Pick winner with rationale | sonnet | Multi-criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reranker-config.yaml` | Reranker config + warmup hook + fallback policy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking-models.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[reranking-two-stage]]
- [[reranking-pipeline-integration]]
- [[reranking-diversity-mmr]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks reranker type by traffic, self-host policy, and recall need. Each leaf references a rule id from `01-core-rules.xml`.
