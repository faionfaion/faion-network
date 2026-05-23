# Earned Value Management

## Summary

**One-sentence:** Integrates scope/schedule/cost into PV, EV, AC with indices (SPI, CPI) and forecasts (EAC, TCPI) to predict final cost and completion date.

**One-paragraph:** Integrates scope/schedule/cost into PV, EV, AC with indices (SPI, CPI) and forecasts (EAC, TCPI) to predict final cost and completion date. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-earned-value-management.py` enforces the output contract.

**Ефективно для:**

- Capital programs with monthly steering and locked baselines.
- Government / defence programs where EVM compliance is contractual.
- Multi-phase programs needing objective progress vs schedule + budget.
- Forecasting EAC + completion date with mathematical defensibility.

## Applies If (ALL must hold)

- Cost + schedule baselines published.
- Each work package has a measurement method (0/100, 50/50, % complete, milestone).
- Actual cost data available per accounting period.

## Skip If (ANY kills it)

- Agile delivery without baselines — use velocity + burn-up.
- No actual-cost feed from finance — EVM is unreliable.
- Project <$100k — EVM overhead exceeds insight.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cost baseline (PV curve) | JSON/CSV with cumulative PV per period | PM + Finance |
| EV measurement method per package | dict slug → method | PM |
| AC per period | CSV from finance system | Finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | PV curve is built from the cost estimate |
| [[project-integration]] | EVM is the integrator's pulse |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-evm` | haiku | Mechanical EVM formulae. |
| `forecast-eac` | sonnet | Judgement on EAC formula selection (CPI, SPI*CPI, etc.). |
| `draft-evm-narrative` | sonnet | Narrative tied to variance > thresholds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-report.md` | EVM report template: PV, EV, AC, SPI, CPI, EAC, TCPI per period |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-earned-value-management.py` | Validate the report artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[cost-estimation]]
- [[project-integration]]
- [[benefits-realization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

