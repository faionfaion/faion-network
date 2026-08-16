# North Star Metric Design

## Summary

**One-sentence:** Designs a single North Star Metric: candidate generation, leading-vs-lagging classification, formula + cadence + owner; output is an NSM spec ready for KPI-tree cascade.

**One-paragraph:** Designs a single North Star Metric: candidate generation, leading-vs-lagging classification, formula + cadence + owner; output is an NSM spec ready for KPI-tree cascade. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Pre-PMF startup needs one growth metric the whole team can rally around.
- Post-PMF company swapping vanity metrics for one outcome-aligned NSM.
- Quarterly strategy refresh: re-anchor every team OKR to a single NSM.
- Investor / board comms: pin one number that explains progress quarter on quarter.

## Applies If (ALL must hold)

- Product has ≥1 month of usage data to back candidate metrics.
- ≥3 candidate metrics already brainstormed by team.
- Customer value hypothesis is one sentence ('users get X by doing Y').
- Leadership has authority to retire competing 'north star' candidates.

## Skip If (ANY kills it)

- Pre-product or no usage data — NSM would be aspirational, use a goal instead.
- Multiple products with disjoint user bases — design NSM per product.
- Customer value hypothesis is unclear — apply pmf-rubric-for-solos first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate metrics list | list of {name, formula, cadence} | team workshop |
| Usage data sample | 1 month of activity events | warehouse |
| Customer value hypothesis | one-sentence statement | founder / product |
| Leadership sign-off authority | named person + email | org chart |

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
| `draft-north-star-metric-design` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md.j2` | Markdown skeleton conforming to the output contract |
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract Generated from `templates/artefact-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-north-star-metric-design.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[kpi-tree-construction]]
- [[north-star-vs-okr-confidence-calibration]]
- [[pmf-rubric-for-solos]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "nsm_id": "nsm-acme-2026q2",
  "owner": "cpo@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "candidates": [
    {
      "name": "weekly_active_users",
      "formula": "count(distinct user_id where active_7d=true)",
      "type": "leading",
      "evidence": "BI table fct_activity"
    },
    {
      "name": "monthly_revenue",
      "formula": "sum(stripe_charges where month=this_month)",
      "type": "lagging",
      "evidence": "Stripe export 2026-05"
    },
    {
      "name": "weekly_engaged_minutes",
      "formula": "sum(minutes_per_user where active_7d=true)",
      "type": "leading",
      "evidence": "BI table fct_engagement"
    }
  ],
  "selected": "weekly_engaged_minutes",
  "rationale": "leading indicator + ties to value hypothesis 'users save time by doing X'",
  "formula": "sum(minutes_per_user where active_7d=true)",
  "cadence": "weekly",
  "review_cadence": "quarterly NSM review",
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
