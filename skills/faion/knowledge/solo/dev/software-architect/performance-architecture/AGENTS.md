---
slug: performance-architecture
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design systems to meet explicit SLO targets (p50/p95/p99, throughput, error rate, availability) by addressing all five layers: client, CDN/edge, load balancer, application, and data.
content_id: "ab7f78da35a65132"
tags: [performance, slo, scalability, load-testing, optimization]
---
# Performance Architecture

## Summary

**One-sentence:** Design systems to meet explicit SLO targets (p50/p95/p99, throughput, error rate, availability) by addressing all five layers: client, CDN/edge, load balancer, application, and data.

**One-paragraph:** Design systems to meet explicit SLO targets (p50/p95/p99, throughput, error rate, availability) by addressing all five layers: client, CDN/edge, load balancer, application, and data. Run a measurement-first loop: profiler agent reads APM/traces → analyzer identifies bottleneck layer → designer proposes change with predicted p95 improvement → validator runs a load test that proves or disproves the prediction. Never optimize without a captured baseline.

## Applies If (ALL must hold)

- Defining SLOs and error budgets at design time, before performance becomes a customer complaint.
- Pre-launch capacity planning for a feature expected to receive measurable traffic.
- Performance regression triage: structured layer-by-layer narrowing.
- Cost optimization driven by tail latency or compute waste.
- Pre-IPO/audit scenarios requiring documented performance commitments.

## Skip If (ANY kills it)

- Pure prototypes — premature optimization slows delivery without buying reliability.
- Pages/APIs with no production traffic yet — measure first.
- Hot-fixing a single slow query — use profiling tools directly, not a full architecture loop.

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
