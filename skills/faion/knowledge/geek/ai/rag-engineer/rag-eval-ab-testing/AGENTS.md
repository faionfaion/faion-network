---
slug: rag-eval-ab-testing
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing for RAG configurations runs the same question set through two pipeline variants and compares their results.
content_id: "ec005996c19dff9a"
tags: [rag, ab-testing, evaluation, configuration]
---
# RAG A/B Testing Framework

## Summary

**One-sentence:** A/B testing for RAG configurations runs the same question set through two pipeline variants and compares their results.

**One-paragraph:** A/B testing for RAG configurations runs the same question set through two pipeline variants and compares their results. The baseline framework measures latency and source count; a full quality comparison requires integrating the RAGAS evaluation loop per configuration. Use A/B testing to validate parameter changes (chunk size, embedding model, top-K, reranker) before promoting config B to production.

## Applies If (ALL must hold)

- Comparing different chunk sizes (e.g., 500 vs 1000 tokens) for the same corpus.
- Evaluating the impact of adding or swapping a reranker model.
- Comparing embedding models (text-embedding-3-large vs voyage-3) on retrieval quality.
- Validating any config parameter change before promoting it to production.

## Skip If (ANY kills it)

- When the test set has fewer than 20 questions — sample size is too small for reliable comparison; differences are within noise.
- When the two configurations are not isolated — if they share index state or caches, results are not comparable.
- When only comparing latency matters and quality is irrelevant — skip A/B testing, just benchmark directly.

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

- parent skill: `geek/ai/rag-engineer/`
