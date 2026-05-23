---
slug: cost-estimation
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defensible bottom-up cost baseline: WBS decomposition, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and separate management reserve.
content_id: "5b4a3c2d1e0f9a8b"
complexity: deep
produces: spec
est_tokens: 5200
tags: [estimation, budget, cost-baseline, wbs, pert]
---
# Cost Estimation

## Summary

**One-sentence:** Defensible bottom-up cost baseline: WBS decomposition, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and separate management reserve.

**One-paragraph:** Defensible bottom-up cost baseline: WBS decomposition, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and separate management reserve.

**Ефективно для:**

- Запитів на фіксовану ціну, де PM зобов'язаний захистити кошторис.
- Внутрішнього budget approval з ROI-orientation.
- Контрактів типу cost-plus з documented baseline.
- Програм, де cost variance — KPI keypoint у performance reviews.

## Applies If (ALL must hold)

- Project value ≥ 25k requires defensible cost baseline.
- WBS or feature-level decomposition is producible.
- Historical similar-engagement data is reachable.
- Buyer signs off on the estimate before kick-off.

## Skip If (ANY kills it)

- Time-and-materials no-cap engagement.
- Internal R&D spike under 40 hours.
- Fully fixed-team retainer with no per-project cost question.
- Highly novel domain with zero prior data — use exploratory budget, not PERT.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-leverage-estimation-model]] | Multiplier rubric applied AFTER raw PERT estimate. |
| [[earned-value-management]] | EVM consumes this baseline for tracking. |

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
| `wbs-decompose` | sonnet | Decompose scope into leaves with success criteria. |
| `pert-estimate` | sonnet | Three-point estimation per leaf with rationale. |
| `reserve-sizing` | opus | Risk-driven contingency + management reserve. |
| `baseline-validate` | haiku | Run validator and emit baseline document. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-worksheet.md` | Bottom-up worksheet: leaf, optimistic, most-likely, pessimistic, PERT, risk. |
| `templates/quick-estimate.md` | 10-line estimate skeleton for early-phase ballparking. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-estimation.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[ai-leverage-estimation-model]]
- [[earned-value-management]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (project_value_band, scope_frozen, historical_data_available) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
