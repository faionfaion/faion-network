---
slug: earned-value-management
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: EVM is an objective, formula-driven approach to project performance measurement.
content_id: "e613e20980b40046"
tags: [evm, project-management, performance-metrics, forecasting, cost-control]
---
# Earned Value Management

## Summary

**One-sentence:** EVM is an objective, formula-driven approach to project performance measurement.

**One-paragraph:** EVM is an objective, formula-driven approach to project performance measurement. It combines three primary inputs (Planned Value, Earned Value, Actual Cost) to produce variance metrics (SV, CV, SPI, CPI) and forecasts (EAC, ETC, TCPI). The single biggest rule: use objective % complete only — milestones, units completed, or 0/50/100 rules — never subjective opinion, which corrupts EV and cascades into false forecasts.

## Applies If (ALL must hold)

- Predictive/hybrid projects with a fixed scope baseline and budget.
- Programs with monthly/weekly steering committee status reporting that require objective trend, not narrative.
- Government, defense, infrastructure, large IT — contracts that require ANSI/EIA-748 or similar standards.
- Engagements where "% complete" claims have lost credibility and you need an objective measure.
- Program forecasting (EAC/ETC) for board approval of additional budget.

## Skip If (ANY kills it)

- Pure agile teams shipping continuously — burndown and flow metrics are better fits.
- Discovery/R&D phases with no stable baseline to measure against.
- Projects under 6 weeks or under $50k — overhead exceeds insight gained.
- Internal startup work where speed matters more than financial control.
- Soft-cost projects with no convertible-to-dollars effort tracking.

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
