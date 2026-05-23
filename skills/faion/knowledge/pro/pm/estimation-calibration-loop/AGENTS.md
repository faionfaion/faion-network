---
slug: estimation-calibration-loop
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Quarterly calibration artefact: estimate-vs-actual per task class, bias per estimator, suggested factor adjustment, target accuracy band, next review trigger.
content_id: "8d1b97c2ee5c4446"
complexity: medium
produces: report
est_tokens: 5200
tags: [pm, pro, estimation, calibration, metrics, retrospective]
---
# Estimation Calibration Loop

## Summary

**One-sentence:** Quarterly calibration artefact: estimate-vs-actual per task class, bias per estimator, suggested factor adjustment, target accuracy band, next review trigger.

**One-paragraph:** Estimation Calibration Loop delivers a defensible report artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Команди з історією 60+ днів estimate-vs-actual і атрибуцією estimator-а.
- Outsource agency, що бідає фіксовану ціну і має eroding margin issue.
- Founder-PM з 3-5 девелоперами та власною velocity-data, який хоче перейти від guesswork до math.
- PMO, що калібрує velocity for portfolio-level forecasting, не лише single-sprint.

## Applies If (ALL must hold)

- task estimates exist with corresponding recorded actuals (last 60+ days)
- estimator attribution is preserved (per person or per role) for bias detection
- team commits to acting on the loop's output (factor adjustment, retraining, scope rules)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- no recorded actuals — calibration impossible; fix the tracking first
- estimates are anonymous — bias attribution would invent estimators
- team is one person doing variable work — sample size too small to be useful

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-estimation_calibration_loop` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/estimation-calibration-loop.md` | report skeleton with required fields + 5-line header |
| `templates/estimation-calibration-loop.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-estimation-calibration-loop.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[fixed-price-three-point-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
