---
slug: embedding-cost-optimization
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Five levers reduce embedding API cost without sacrificing retrieval quality: dimension reduction, batch API requests, aggressive caching, two-stage retrieval using a cheap filter model, and deduplication before ingestion.
content_id: "9b9e945ccf1c6435"
tags: [embeddings, cost-optimization, rag, batching, deduplication]
---
# Embedding Cost Optimization

## Summary

**One-sentence:** Five levers reduce embedding API cost without sacrificing retrieval quality: dimension reduction, batch API requests, aggressive caching, two-stage retrieval using a cheap filter model, and deduplication before ingestion.

**One-paragraph:** Five levers reduce embedding API cost without sacrificing retrieval quality: dimension reduction, batch API requests, aggressive caching, two-stage retrieval using a cheap filter model, and deduplication before ingestion. Applied together, typical savings exceed 80%.

## Applies If (ALL must hold)

- Embedding API cost is measurable on the monthly bill.
- Large corpus ingestion (more than 100K documents).
- High-frequency re-ingestion with stable documents (incremental updates).
- Two-stage retrieval patterns where first-pass recall can tolerate a cheaper model.

## Skip If (ANY kills it)

- Small one-time ingestion (fewer than 10K documents) — optimization overhead exceeds savings.
- Domain where quality is critical and cheaper models have not been benchmarked — do not substitute without measuring retrieval metrics.

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
