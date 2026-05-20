---
slug: serverless-cold-start-optimization
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cold starts occur when a new Lambda function instance is created (no warm container exists).
content_id: "2c70ffda1c3e52f3"
tags: [serverless, cold-start, performance, lambda, optimization]
---
# Serverless Cold Start Optimization

## Summary

**One-sentence:** Cold starts occur when a new Lambda function instance is created (no warm container exists).

**One-paragraph:** Cold starts occur when a new Lambda function instance is created (no warm container exists). Mitigation ranges from code-level patterns (init outside handler, smaller packages) to infrastructure choices (provisioned concurrency, SnapStart, ARM/Graviton). The correct fix depends on the runtime, traffic pattern, and latency SLO.

## Applies If (ALL must hold)

- Cold start rate exceeds 10% for user-facing Lambda functions.
- p95 latency spikes are traced to cold start events in X-Ray or Lumigo.
- Adopting Java, .NET, or large Python/Node packages in a Lambda that must respond in <2s.
- Evaluating whether provisioned concurrency ROI justifies the cost for a given function.

## Skip If (ANY kills it)

- Background processing functions (Kinesis consumers, SQS workers) where latency variance is irrelevant — cold starts do not affect user experience.
- Batch or scheduled jobs — cold start is a one-time cost amortized over the batch duration.
- Functions already using provisioned concurrency that are meeting their SLOs — further optimization has diminishing returns.

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
