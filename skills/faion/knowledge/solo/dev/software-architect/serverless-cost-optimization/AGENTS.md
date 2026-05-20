---
slug: serverless-cost-optimization
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Lambda cost equals Requests + (Duration × Memory) + Data Transfer.
content_id: "efd6b994a5593d12"
tags: [serverless, cost, lambda, finops, optimization]
---
# Serverless Cost Optimization

## Summary

**One-sentence:** Lambda cost equals Requests + (Duration × Memory) + Data Transfer.

**One-paragraph:** Lambda cost equals Requests + (Duration × Memory) + Data Transfer. ARM/Graviton saves 20%, right-sizing memory (via Lambda Power Tuning) saves 10-50%, and batch processing saves 30-70%. The container crossover point is roughly 10-30M requests/month at consistent load. Cost monitoring with per-function granularity is mandatory for production workloads.

## Applies If (ALL must hold)

- Estimating and projecting Lambda costs before or during architecture design.
- Monthly cost review for production serverless workloads.
- Evaluating the cost/performance tradeoff of switching to ARM/Graviton.
- Analyzing whether to migrate a high-volume workload from Lambda to containers.
- Optimizing a Lambda function identified as a cost anomaly in Cost Explorer.

## Skip If (ANY kills it)

- Newly launched functions with no traffic data — cost projections require baseline measurements.
- One-off scripts or developer tooling — cost is trivial and optimization is not worth the effort.

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

- parent skill: `solo/dev/software-architect/`
