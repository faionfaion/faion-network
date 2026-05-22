---
slug: embeddings-evaluation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: MTEB scores are general benchmarks — always benchmark on your specific data.
content_id: "f5e373e0824a5c49"
tags: [embeddings, evaluation, benchmarking, recall, rag]
---
# Embedding Quality Evaluation and Benchmarking

## Summary

**One-sentence:** MTEB scores are general benchmarks — always benchmark on your specific data.

**One-paragraph:** MTEB scores are general benchmarks — always benchmark on your specific data. Create an evaluation set of 100-500 real query-document pairs, test at least 3-4 candidate models, measure Recall@K and MRR, then run an A/B test in production before full rollout. Without a domain-specific evaluation, model selection is guesswork.

## Applies If (ALL must hold)

- Selecting an embedding model for a new project (always).
- Evaluating whether to switch from one model to another.
- Diagnosing poor retrieval quality in production.
- Validating a model update before re-embedding the full corpus.

## Skip If (ANY kills it)

- Prototype with fewer than 50 documents — use any reasonable model and defer evaluation.
- When you cannot create a query-document evaluation set — fall back to MTEB scores with domain-awareness caveats.

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
