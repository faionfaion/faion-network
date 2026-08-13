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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "experiment_id": "px-acme-tier-2026q2",
  "owner": "pricing@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "hypothesis": "Raising Pro from $19 to $29 lifts ARPU by 30% with <10% conversion loss",
  "cohorts": [
    {
      "id": "c-new-signups-eu",
      "filter": "country in eu and signup > 2026-05-24"
    }
  ],
  "variants": [
    {
      "id": "a",
      "price": 19
    },
    {
      "id": "b",
      "price": 29
    }
  ],
  "metrics": {
    "primary": "checkout_conversion",
    "secondary": [
      "arpu",
      "refund_rate"
    ]
  },
  "grandfathering": {
    "policy": "existing customers locked at $19 for 12 months",
    "evidence": "policy memo 2026-05-22"
  },
  "power_analysis": {
    "expected_effect": 0.3,
    "mde": 0.1,
    "target_n": 8000
  },
  "legal_clearance": {
    "reviewer": "legal@acme.io",
    "memo": "drive://legal/price-test-eu-2026.pdf"
  },
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
