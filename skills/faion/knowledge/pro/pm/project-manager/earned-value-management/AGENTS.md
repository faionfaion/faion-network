---
slug: earned-value-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Formula-driven performance measurement: PV/EV/AC with CPI, SPI, EAC, TCPI metrics to forecast cost-at-completion and trigger corrective action when CPI or SPI drift below 0.9.
content_id: "ae3f8b9c2d1e4f5a"
complexity: deep
produces: report
est_tokens: 5100
tags: [evm, performance-metrics, forecasting, cost-control]
---
# Earned Value Management

## Summary

**One-sentence:** Formula-driven performance measurement: PV/EV/AC with CPI, SPI, EAC, TCPI metrics to forecast cost-at-completion and trigger corrective action when CPI or SPI drift below 0.9.

**One-paragraph:** Formula-driven performance measurement: PV/EV/AC with CPI, SPI, EAC, TCPI metrics to forecast cost-at-completion and trigger corrective action when CPI or SPI drift below 0.9.

**Ефективно для:**

- Контрактів cost-plus, де клієнт вимагає monthly EVM.
- Програм з фіксованим бюджетом і timeline, де cost variance — головний KPI.
- PMO з ≥5 одночасних проектів, де порівняти прогрес можна тільки через нормалізовані метрики.
- Регульованих індустрій (DoD, аерокосмос), де EVMS — частина контракту.

## Applies If (ALL must hold)

- Cost baseline exists and is approved.
- Schedule baseline exists with planned-value curve.
- Actuals (AC) can be collected per reporting period.
- Reporting cadence weekly or monthly.

## Skip If (ANY kills it)

- Agile/Scrum team with rolling-wave planning.
- T&M engagement with no fixed baseline.
- Project value &lt;100k — EVM overhead exceeds benefit.
- Single-person project — variance signal is too noisy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | PERT baseline forms the PV curve. |
| [[change-control]] | Re-baseline events recorded via CR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pv-curve-author` | sonnet | Build planned-value curve from baseline + schedule. |
| `ev-collector` | haiku | Pull earned-value from task completion log. |
| `variance-analyzer` | sonnet | Compute CPI, SPI, EAC, TCPI, flag thresholds. |
| `corrective-action-recommender` | opus | Synthesize corrective action when CPI/SPI &lt;0.9. |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-report.md` | Period report: PV, EV, AC, CPI, SPI, EAC, TCPI table + variance narrative. |
| `templates/pv-curve.csv` | Time-phased planned-value curve. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-earned-value-management.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[cost-estimation]]
- [[change-control]]
- [[predictive-analytics-pm]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (baselines_exist, reporting_cadence, project_value_band) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
