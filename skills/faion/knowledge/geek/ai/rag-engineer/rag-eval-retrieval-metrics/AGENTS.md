---
slug: rag-eval-retrieval-metrics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Computes Precision@K, Recall@K, MRR, NDCG and hit-rate for a RAG retrieval pass and exports a per-query JSONL.
content_id: "85295da758e470f5"
complexity: medium
produces: report
est_tokens: 3000
tags: [rag, evaluation, retrieval, metrics, information-retrieval]
---
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
