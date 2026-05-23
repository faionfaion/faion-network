---
slug: predictive-analytics-pm
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Forecast report applying ML-based prediction to schedule delay, budget overrun, resource utilisation, and risk pattern mining from issue tracker data, with calibration metrics."
content_id: "fbb62d16d1726dde"
complexity: medium
produces: report
est_tokens: 4500
tags: [predictive-analytics, forecasting, ml, risk-management, pm]
---
# Predictive Analytics for PM

## Summary

**One-sentence:** Forecast report applying ML-based prediction to schedule delay, budget overrun, resource utilisation, and risk pattern mining from issue tracker data, with calibration metrics.

**One-paragraph:** Predictive Analytics for PM defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Programs with >=12 weeks of issue-tracker history (statistical signal exists).
- PMs who want a defensible early-warning signal beyond gut feel.
- Portfolio leads benchmarking multiple programs on uniform metrics.
- Risk owners wanting pattern-mining over historical issues.

## Applies If (ALL must hold)

- >=12 weeks of clean issue tracker data with timestamps + state changes.
- A data engineer or analyst can implement the forecasting pipeline.
- Calibration history available (prior forecasts + actual outcomes).
- Decision owner accepts probabilistic forecasts (not point estimates).

## Skip If (ANY kills it)

- Issue tracker data is dirty (state transitions missing, no timestamps) — fix data first.
- Project lifetime <12 weeks — too little data to forecast.
- Decision owner insists on deterministic estimates — predictive analytics will be rejected on delivery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `predictive-analytics-pm_template_fill` | haiku | Bounded template fill, no judgement. |
| `predictive-analytics-pm_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `predictive-analytics-pm_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the predictive analytics forecast artefact. |
| `templates/calibration.py` | Reference script computing calibration score against prior forecasts. |
| `templates/forecast-report.md` | Markdown skeleton for the forecast report with predictions table + calibration block. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-predictive-analytics-pm.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
