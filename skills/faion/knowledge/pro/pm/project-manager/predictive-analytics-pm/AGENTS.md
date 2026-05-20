---
slug: predictive-analytics-pm
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Apply machine learning to historical project data to generate early-warning signals for schedule slip, budget overrun, resource contention, and material price risk — turning raw PM telemetry into probability-interval forecasts that change PMO decisions before events occur.
content_id: "77a993decd968d13"
tags: [predictive-analytics, machine-learning, risk-forecasting, evm, data-science]
---
# Predictive Analytics in Project Management

## Summary

**One-sentence:** Apply machine learning to historical project data to generate early-warning signals for schedule slip, budget overrun, resource contention, and material price risk — turning raw PM telemetry into probability-interval forecasts that change PMO decisions before events occur.

**One-paragraph:** Apply machine learning to historical project data to generate early-warning signals for schedule slip, budget overrun, resource contention, and material price risk — turning raw PM telemetry into probability-interval forecasts that change PMO decisions before events occur. The analytics layer lives in a separate ML pipeline feeding the PM tool through alerts and dashboards; humans retain all decision authority.

## Applies If (ALL must hold)

- Portfolio of 50+ comparable projects with 12+ months of clean historical data (issues, time logs, budget actuals)
- Construction, engineering, manufacturing, or infrastructure programs where slip and overrun are repeat offenders
- PMO needs early-warning dashboard and executive trend signals
- Vendor/commodity-heavy programs where price volatility (steel, cloud spend) drives budget risk
- EVM already in place and the org wants an ML complement for interval forecasting

## Skip If (ANY kills it)

- Portfolio under 10 projects — sample size is too small; use heuristics + EVM instead
- Brand-new project type with no historical analogues — no training data; use reference-class forecasting alone
- Highly creative or one-off work (research, novel product) — past patterns do not generalize
- Organisation without basic data hygiene (inconsistent statuses, missing actuals, freeform fields) — fix data first
- Goal is optics ("look modern") rather than changing actual PMO decisions — model value requires action on output

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
