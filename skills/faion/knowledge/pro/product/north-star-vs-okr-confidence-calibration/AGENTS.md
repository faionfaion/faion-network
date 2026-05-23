---
slug: north-star-vs-okr-confidence-calibration
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a weekly confidence-calibration report mapping current OKR progress against NSM target with explicit risks; output is a forecast report with named owners and intervention triggers.
content_id: "0a6e70b440b22396"
complexity: medium
produces: report
est_tokens: 5400
tags: [product, pro, okr, calibration, forecast, report]
---
# North Star vs OKR Confidence Calibration

## Summary

**One-sentence:** Produces a weekly confidence-calibration report mapping current OKR progress against NSM target with explicit risks; output is a forecast report with named owners and intervention triggers.

**One-paragraph:** Produces a weekly confidence-calibration report mapping current OKR progress against NSM target with explicit risks; output is a forecast report with named owners and intervention triggers. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Weekly product metrics review needs honest confidence number per KR.
- Quarterly OKR check-in: is the NSM trend on-pace, lagging, or off-pace.
- Investor / board: pre-empt awkward surprises with calibrated forecasts.
- Team morale: visible drift in confidence triggers help-asks early, not at end of quarter.

## Applies If (ALL must hold)

- Active quarterly OKRs with measurable KRs ladder up to the NSM.
- ≥4 weeks of OKR progress data available.
- Named owner per KR exists and reviews progress weekly.
- Forecast model (linear projection or better) can be applied to KR data.

## Skip If (ANY kills it)

- No active OKRs — apply okr-design methodology first.
- OKRs not measurable (vanity / aspirational) — fix OKRs first.
- <4 weeks of data — projection is noise, not signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OKR list | list of {okr, kr, target, current, owner} | OKR tool / sheet |
| Weekly progress snapshots | ≥4 weekly KR values | BI / sheet |
| NSM target | quarter-end NSM goal | leadership |
| Owner roster | KR -> owner email | org chart |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-north-star-vs-okr-confidence-calibration` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-north-star-vs-okr-confidence-calibration.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[north-star-metric-design]]
- [[kpi-tree-construction]]
- [[post-launch-72h-watch-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
