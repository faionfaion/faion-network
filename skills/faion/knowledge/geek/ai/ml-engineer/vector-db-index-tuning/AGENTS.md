---
slug: vector-db-index-tuning
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure HNSW index parameters (M, ef_construct, ef_search), choose a quantization strategy (scalar int8, product, binary), and select workload profiles (read-heavy, write-heavy, balanced) to hit defined latency and recall SLAs without over-provisioning memory.
content_id: "98d9b8d37f3e8411"
tags: [vector-database, hnsw, quantization, performance, index-tuning]
---
# Vector Database Index and Quantization Tuning

## Summary

**One-sentence:** Configure HNSW index parameters (M, ef_construct, ef_search), choose a quantization strategy (scalar int8, product, binary), and select workload profiles (read-heavy, write-heavy, balanced) to hit defined latency and recall SLAs without over-provisioning memory.

**One-paragraph:** Configure HNSW index parameters (M, ef_construct, ef_search), choose a quantization strategy (scalar int8, product, binary), and select workload profiles (read-heavy, write-heavy, balanced) to hit defined latency and recall SLAs without over-provisioning memory.

## Applies If (ALL must hold)

- Query latency exceeds the p95 target after initial collection setup.
- Memory usage approaches the instance limit as the vector count grows.
- Recall metrics fall below the defined threshold after enabling quantization.
- Switching between workload profiles (batch indexing to live search).
- Scaling beyond 1M vectors where default parameters cause index quality degradation.

## Skip If (ANY kills it)

- Fewer than 100K vectors — default parameters are fine; tuning overhead is not justified.
- Using a fully managed service (Pinecone Serverless) — the service manages index internals.
- Recall has not been measured — tune recall first, then latency.

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
