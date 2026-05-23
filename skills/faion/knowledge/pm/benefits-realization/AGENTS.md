# Benefits Realization

## Summary

**One-sentence:** Identify, quantify, assign ownership for, and track post-launch business value via a Benefits Register with metrics, baselines, targets, and named owners accountable after delivery.

**One-paragraph:** Identify, quantify, assign ownership for, and track post-launch business value via a Benefits Register with metrics, baselines, targets, and named owners accountable after delivery.

**Ефективно для:**

- Бізнес-кейсів, що вимагають quantified ROI з tracking-plan.
- Post-launch portfolio reviews (3, 6, 12 months) у PMO.
- Інвестиційних комітетів, що ставлять питання payback.
- Програм, де outputs передають outcomes на 6-18 місяців.

## Applies If (ALL must hold)

- Business case approval requires quantified ROI + tracking plan.
- Post-launch portfolio review across ≥3 projects scheduled.
- Benefit owner is a business stakeholder, NOT the PM.
- Baseline values can be measured before launch.

## Skip If (ANY kills it)

- Pre-revenue startup pre-PMF — benefits are speculative.
- Compliance-driven project where benefit is binary 'stay legal'.
- Internal tooling with no measurable 'before' state.
- Crisis incident response — benefit is 'stopped bleeding'.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | Cost baseline this register multiplies against for ROI. |
| [[earned-value-management]] | Performance-measurement vocabulary used in tracking. |

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
| `benefits-cataloger` | sonnet | Extract quantified benefits from business case prose. |
| `baseline-collector` | haiku | Pull T-0 metric values from source systems. |
| `measurement-runner` | haiku | Periodic pulls vs target, drift detection. |
| `counterfactual-analyzer` | opus | DiD / synthetic-control attribution. |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefits-register.md` | Register table: id, benefit, category, owner, metric, baseline, target, status. |
| `templates/benefits-report.md` | Post-launch report: exec summary, status per benefit, barriers, forecast. |
| `templates/business-case-benefits.md` | Business case section: financial table (3-year), non-financial, ROI/NPV. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-benefits-realization.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[cost-estimation]]
- [[earned-value-management]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (baseline_measurable, owner_is_business_stakeholder, attribution_required) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
