---
slug: pricing-experiment-design
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Designs a live pricing experiment (van Westendorp on traffic, grandfathering, cohort A/B legality, price-sensitivity flags); output is a pricing-experiment design spec.
content_id: "b4c5008e83836b2e"
complexity: deep
produces: spec
est_tokens: 5800
tags: [product, pro, spec, pricing, experiment, growth]
---
# Pricing Experiment Design

## Summary

**One-sentence:** Designs a live pricing experiment (van Westendorp on traffic, grandfathering, cohort A/B legality, price-sensitivity flags); output is a pricing-experiment design spec.

**One-paragraph:** Designs a live pricing experiment (van Westendorp on traffic, grandfathering, cohort A/B legality, price-sensitivity flags); output is a pricing-experiment design spec. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Pricing review: which prices to test on live traffic without breaking trust.
- Pre-launch new tier: validate price point with cohort A/B before public rollout.
- Grandfathering policy: pin existing customer treatment before price change.
- Regulatory check: confirm A/B test legality in target geos (EU consumer law).

## Applies If (ALL must hold)

- Product has ≥1 paid plan with ≥100 paying customers.
- Traffic is sufficient for a 2-week cohort split with statistical power.
- Grandfathering policy can be defined in writing before test launch.
- Legal review available for cohort-segmented price discrimination in target geos.

## Skip If (ANY kills it)

- Pre-revenue or < 100 paying customers — use willingness-to-pay survey instead.
- Traffic too small for power analysis — test will be inconclusive.
- Cannot get legal sign-off in time — block test.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current pricing | tier list with price + features | billing |
| Customer cohort definitions | cohort_id -> filter rule | BI |
| Price hypothesis | candidate prices + expected lift | PM + finance |
| Legal review | memo on A/B price legality in target geos | legal |

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
| `draft-pricing-experiment-design` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pricing-experiment-design.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pricing-experiment-spec-template]]
- [[north-star-metric-design]]
- [[post-launch-72h-watch-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
