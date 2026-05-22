---
slug: value-stream-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Map the end-to-end flow from customer request to customer value, measure it with Flow Metrics (Lead Time, Cycle Time, Throughput, WIP, %C/A) and DORA (Deployment Frequency, Change Lead Time, Change Failure Rate, MTTR), identify the constraint per Theory of Constraints, and run targeted experiments to elevate that constraint.
content_id: "728acb62b35f0f8e"
tags: [flow, dora, metrics, bottleneck, value-stream]
---
# Value Stream Management

## Summary

**One-sentence:** Map the end-to-end flow from customer request to customer value, measure it with Flow Metrics (Lead Time, Cycle Time, Throughput, WIP, %C/A) and DORA (Deployment Frequency, Change Lead Time, Change Failure Rate, MTTR), identify the constraint per Theory of Constraints, and run targeted experiments to elevate that constraint.

**One-paragraph:** Map the end-to-end flow from customer request to customer value, measure it with Flow Metrics (Lead Time, Cycle Time, Throughput, WIP, %C/A) and DORA (Deployment Frequency, Change Lead Time, Change Failure Rate, MTTR), identify the constraint per Theory of Constraints, and run targeted experiments to elevate that constraint. Instrument with telemetry first — a VSM workshop without data decays into a poster within months.

## Applies If (ALL must hold)

- Engineering org has shipped DevOps automation but customer-visible lead time has not improved
- Cross-functional bottleneck suspected across product → design → eng → release → support
- Quarterly OKR cycle wants to move from output metrics to flow metrics
- DORA metrics are already in place but not improving — need upstream view via Flow Metrics
- Org adopting SAFe, FAST Agile, or the Project-to-Product model

## Skip If (ANY kills it)

- Single-team, single-product startup pre-PMF — premature optimization
- Org without telemetry baseline (no commit timestamps, no deploy log) — instrument first
- Pure cost-cutting context — VSM exposes inefficiencies but is not a layoff lever
- Teams with no shared ownership across the stream — VSM names the bottleneck but cannot move it

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

- parent skill: `pro/pm/project-manager/`
