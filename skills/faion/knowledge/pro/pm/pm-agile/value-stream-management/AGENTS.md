---
slug: value-stream-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Value Stream Management (VSM) maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput.
content_id: "728acb62b35f0f8e"
tags: [value-stream, flow-metrics, dora, bottleneck, theory-of-constraints]
---
# Value Stream Management

## Summary

**One-sentence:** Value Stream Management (VSM) maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput.

**One-paragraph:** Value Stream Management (VSM) maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput. Paired with DORA metrics for the DevOps stages, VSM reveals where AI productivity gains evaporate into cross-functional bottlenecks invisible to per-team metrics. The rule: always report Flow Metrics and DORA together; never present one alone to executives.

## Applies If (ALL must hold)

- Programs where local team optimization no longer produces business throughput gains.
- Boards report "green" velocity but customer time-to-value is stuck.
- AI productivity rollout raised dev velocity but lead time did not decrease (productivity paradox).
- DevOps maturity reviews requiring a complete picture beyond DORA.
- Multi-team programs (SAFe Value Streams, ARTs) where VSM is foundational.

## Skip If (ANY kills it)

- Single team, single product, short cycle times — VSM overhead exceeds insight value.
- Data quality too poor to trust (status-field abuse, transitions not captured) — fix discipline first.
- Culture where metrics will be weaponized for individual performance management — VSM dies on first quarterly review.
- Pure research / discovery work where "value" is exploratory; VSM optimizes known-work flow.
- Bottleneck is known and political (approval committee) and leadership won't intervene — measuring changes nothing.

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

- parent skill: `pro/pm/pm-agile/`
