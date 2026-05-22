---
slug: earned-value-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Earned Value Management (EVM) measures project performance by integrating scope, schedule, and cost into three numbers — Planned Value (PV), Earned Value (EV), and Actual Cost (AC) — and derives objective indices (SPI, CPI) and forecasts (EAC, TCPI) that predict final cost and completion date.
content_id: "e613e20980b40046"
tags: [earned-value-management, performance-measurement, project-control, forecasting, pmbok]
---
# Earned Value Management

## Summary

**One-sentence:** Earned Value Management (EVM) measures project performance by integrating scope, schedule, and cost into three numbers — Planned Value (PV), Earned Value (EV), and Actual Cost (AC) — and derives objective indices (SPI, CPI) and forecasts (EAC, TCPI) that predict final cost and completion date.

**One-paragraph:** Earned Value Management (EVM) measures project performance by integrating scope, schedule, and cost into three numbers — Planned Value (PV), Earned Value (EV), and Actual Cost (AC) — and derives objective indices (SPI, CPI) and forecasts (EAC, TCPI) that predict final cost and completion date. All computation is deterministic; LLMs narrate, they never calculate.

## Applies If (ALL must hold)

- Fixed-price or cost-plus contracts requiring DCMA/DCAA compliance (defense, aerospace, government)
- Capital programs with multi-year baselines where SPI/CPI trends feed quarterly board reporting
- Programs where percent-complete claims have been chronically inflated
- Hybrid/agile programs that still need finance-grade burn forecasts (EAC, ETC, VAC) tied to velocity
- Portfolio reporting where many projects feed a single rollup

## Skip If (ANY kills it)

- Pre-PMF startups or pure agile teams without baseline budgets — EVM math is meaningless without a credible PV curve
- Time-and-materials contracts where only AC matters — EVM adds overhead with no decision impact
- Discovery or spike phases where "percent complete" is undefined
- Projects under one quarter with a single team — burndown and weekly retro provide the same insight cheaper
- Projects without WBS or work-package-level budgets — EVM rolls up from packages; without them the metrics are fiction

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

- parent skill: `pro/pm/pm-traditional/`
