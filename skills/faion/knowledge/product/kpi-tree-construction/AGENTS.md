# KPI Tree Construction

## Summary

**One-sentence:** Decomposes an NSM into a navigable tree where every leaf has owner, formula, cadence and evidence link; output is a validated KPI tree spec.

**One-paragraph:** Decomposes an NSM into a navigable tree where every leaf has owner, formula, cadence and evidence link; output is a validated KPI tree spec. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Cascade an annual OKR into weekly leaf metrics each with named owner.
- Eject vanity metrics by forcing formula + data-source per leaf node.
- Audit existing KPI dashboards for orphan metrics with no decision attached.
- Onboard new hire fast: tree shows what they own and what feeds their leaf.

## Applies If (ALL must hold)

- North Star Metric (NSM) already defined and agreed.
- Team has ≥3 functions whose work should ladder into the NSM.
- Data infra exists to compute candidate leaf metrics weekly.
- Each candidate leaf has a plausible named owner.

## Skip If (ANY kills it)

- No NSM defined yet — apply north-star-metric-design first.
- Team size < 3 — overhead exceeds value, use a flat 5-metric list.
- Data infra cannot compute weekly — metrics will rot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| NSM definition | one-line statement with formula and cadence | leadership |
| Function list | list of functions with lead names | org chart |
| Data warehouse spec | list of computable metrics with source table | data team |
| Existing dashboards | list of metrics currently tracked | BI tool export |

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
| `draft-kpi-tree-construction` | sonnet | Output drafting needs structure + light judgement. |
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
| `scripts/validate-kpi-tree-construction.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[north-star-metric-design]]
- [[north-star-vs-okr-confidence-calibration]]
- [[pmf-rubric-for-solos]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "tree_id": "kpi-acme-2026q2",
  "owner": "cpo@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "north_star": {
    "name": "weekly_active_subscribers",
    "formula": "count(distinct user_id where active_in_7d=true and sub_active=true)",
    "cadence": "weekly",
    "evidence": "BI table fct_subscribers"
  },
  "nodes": [
    {
      "id": "n-1",
      "name": "activation_rate",
      "owner": "growth-lead",
      "formula": "activated / signed_up",
      "cadence": "weekly",
      "parent": "north_star",
      "evidence": "BI view dim_activation"
    },
    {
      "id": "n-2",
      "name": "weekly_engagement",
      "owner": "product-lead",
      "formula": "engaged_in_7d / active",
      "cadence": "weekly",
      "parent": "north_star",
      "evidence": "BI view fct_engagement"
    },
    {
      "id": "n-3",
      "name": "monthly_retention",
      "owner": "cs-lead",
      "formula": "retained_m1 / cohort_size",
      "cadence": "monthly",
      "parent": "north_star",
      "evidence": "BI view fct_retention"
    }
  ],
  "edges": [
    {
      "from": "n-1",
      "to": "north_star"
    },
    {
      "from": "n-2",
      "to": "north_star"
    },
    {
      "from": "n-3",
      "to": "north_star"
    }
  ],
  "review_cadence": "weekly review every Friday 30 min",
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
