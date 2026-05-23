---
slug: predictive-analytics-pm
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Apply machine learning to historical project data for early-warning signals (schedule slip, budget overrun, resource contention, material price risk), producing probability-interval forecasts that change PMO decisions before events occur.
content_id: "e7f8a9b0c1d2e3f4"
complexity: deep
produces: spec
est_tokens: 5500
tags: [predictive-analytics, ml, risk-forecasting, evm, data-science]
---
# Predictive Analytics for PM

## Summary

**One-sentence:** Apply machine learning to historical project data for early-warning signals (schedule slip, budget overrun, resource contention, material price risk), producing probability-interval forecasts that change PMO decisions before events occur.

**One-paragraph:** Apply machine learning to historical project data for early-warning signals (schedule slip, budget overrun, resource contention, material price risk), producing probability-interval forecasts that change PMO decisions before events occur.

**Ефективно для:**

- Enterprise PMO з ≥30 проектів історичних даних.
- Construction / aerospace, де material price risk критичний.
- Програм, що поєднують EVM з ML-forecasting.
- Data-science teams, що вбудовують risk models у PMO dashboard.

## Applies If (ALL must hold)

- Historical project portfolio ≥30 completed projects with structured outcome data.
- Data engineering capability available (warehouse, dbt, ML pipeline).
- PMO can act on probability-interval forecasts (not just point estimates).
- Decision-maker accepts model uncertainty disclosure.

## Skip If (ANY kills it)

- &lt;30 historical projects — ML overfits.
- No data-engineering team — model maintenance burden too high.
- Decision-maker rejects probability intervals — wants point estimates.
- Regulatory regime forbids ML-driven decisions in PMO.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[earned-value-management]] | EVM metrics feed the model. |
| [[lessons-learned]] | Post-mortem outcomes label training data. |

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
| `feature-engineer` | opus | Author feature spec from EVM + project metadata. |
| `model-builder` | opus | Train baseline + champion ML model. |
| `calibration-checker` | sonnet | Verify probability calibration on held-out set. |
| `dashboard-wirer` | sonnet | Wire forecasts into PMO dashboard. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-spec.md` | Model card: features, target, training data, calibration metrics, ethics. |
| `templates/forecast-output.json` | Forecast envelope: point + 80% PI + 95% PI per risk dimension. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-predictive-analytics-pm.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[earned-value-management]]
- [[lessons-learned]]
- [[cost-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (history_count, data_eng_capability, decision_acceptance_of_intervals) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
