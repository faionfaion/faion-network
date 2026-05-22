---
slug: performance-testing
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A discipline for validating that applications meet latency, throughput, and stability targets under realistic load.
content_id: "16356ad42913bd38"
tags: [performance, load-testing, benchmarking, profiling, optimization]
---
# Performance Testing

## Summary

**One-sentence:** A discipline for validating that applications meet latency, throughput, and stability targets under realistic load.

**One-paragraph:** A discipline for validating that applications meet latency, throughput, and stability targets under realistic load. Covers five test types (load, stress, spike, endurance, scalability), micro-benchmarking with pytest-benchmark, macro load testing with k6/Locust, profiling with py-spy, and CI budget gates that fail PRs on regression.

## Applies If (ALL must hold)

- Pre-launch validation: API must hold expected RPS at acceptable latency.
- Regression gates after major refactors (ORM swap, query rewrite, caching change).
- Baseline establishment for SLOs (p95 less than 300 ms, error rate less than 1%).
- Capacity planning before scaling infra.
- Endurance soak tests for memory leaks in long-running services.
- Comparing two implementations (orjson vs json, sync vs async ORM).

## Skip If (ANY kills it)

- Pre-MVP code — premature optimization wastes effort.
- One-off scripts or batch jobs without a latency contract.
- Pure UI components without measurable backend interactions.
- Without a staging environment that mirrors prod data volume — results are misleading.
- When the bottleneck is obvious (a single N+1 query EXPLAIN shows clearly).

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

- parent skill: `solo/dev/software-developer/`
