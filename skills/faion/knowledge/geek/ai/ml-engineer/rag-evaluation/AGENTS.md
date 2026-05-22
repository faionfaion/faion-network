---
slug: rag-evaluation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Evaluate Retrieval-Augmented Generation pipelines by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components separately.
content_id: "8a88bfa9e55aa738"
tags: [rag, evaluation, metrics, ragas, retrieval]
---
# RAG Evaluation

## Summary

**One-sentence:** Evaluate Retrieval-Augmented Generation pipelines by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components separately.

**One-paragraph:** Evaluate Retrieval-Augmented Generation pipelines by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components separately. Always evaluate retrieval and generation independently — a high faithfulness score with low hit rate means the model is hallucinating consistently, not retrieving well.

## Applies If (ALL must hold)

- Before promoting a RAG pipeline to production — validate retrieval recall and generation faithfulness.
- After changing chunking strategy, embedding model, or vector DB configuration — check for regression.
- Comparing two embedding models for the same corpus — use Precision@K and MRR to decide.
- Diagnosing user complaints about wrong or hallucinated answers.
- Setting up continuous production monitoring (lightweight faithfulness + hit rate, sampled hourly).

## Skip If (ANY kills it)

- No ground truth queries and the domain is too specialized for reliable synthetic generation.
- Pipeline is a prototype and chunking/embedding strategy is still changing daily — evaluate after it stabilizes.
- Budget is insufficient for LLM-as-judge at scale — use automated retrieval metrics only as a proxy.
- Primary goal is latency optimization, not quality — use profiling tools instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
