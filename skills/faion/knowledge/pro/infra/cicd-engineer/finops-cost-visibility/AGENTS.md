---
slug: finops-cost-visibility
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The INFORM phase establishes the visibility foundation for all FinOps work.
content_id: "22625052bd08eef1"
tags: [finops, cost-allocation, tagging, dashboards, visibility]
---
# FinOps Cost Visibility: Tagging, Allocation, and Dashboards

## Summary

**One-sentence:** The INFORM phase establishes the visibility foundation for all FinOps work.

**One-paragraph:** The INFORM phase establishes the visibility foundation for all FinOps work. It covers mandatory tagging strategy, cost allocation to business units, real-time dashboard setup, and baseline metrics. Without 95%+ tag coverage, all downstream reports are estimates dressed as facts.

## Applies If (ALL must hold)

- Starting a FinOps practice — INFORM is always phase one.
- Tag compliance below 95% — reports are unreliable until this is resolved.
- No per-team or per-product cost breakdown exists.
- Cost anomalies are detected only when the invoice arrives.
- Pre-chargeback: building the showback foundation.

## Skip If (ANY kills it)

- Flat-fee infrastructure where there is no elastic cost to allocate.
- Crisis cost-cutting — apply blunt instruments (shut down non-prod) first, then build visibility.

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

- parent skill: `pro/infra/cicd-engineer/`
