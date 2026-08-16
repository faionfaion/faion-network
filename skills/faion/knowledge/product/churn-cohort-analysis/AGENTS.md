# Churn Cohort Analysis

## Summary

**One-sentence:** Cohort isolation by activation status, leading-indicator detection, save-flow design — the dedicated playbook product-analytics generalities don't provide.

**One-paragraph:** Product-analytics covers cohorts generically; no dedicated playbook for churn cohort isolation by activation, leading indicators, save-flow. Output: churn cohort table + leading-indicator alerts + save-flow design with ≥1 control group.

**Ефективно для:**

- B2B SaaS виявляє churn-pattern, що generic product-analytics пропускає.
- PM cohort-isolates активованих vs. неактивованих з різними remediation playbooks.
- Save-flow design базується на leading indicators, не lagging revenue numbers.

## Applies If (ALL must hold)

- SaaS or subscription product with ≥6 months of paid data
- ≥100 paying customers OR ≥10 paying enterprise accounts
- PM/data has access to activation event tracking (not just MRR)

## Skip If (ANY kills it)

- annual contracts only — different churn cadence; use ARR-renewal patterns
- freemium with no paid layer — there is no churn, only inactivity
- <6 months of data — too noisy for cohort analysis

## Prerequisites

- subscription state table (signup, activate, paid, churn dates)
- activation event definition (concrete behavioral milestone)
- ability to A/B test save-flows or hold out a control

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/product-analytics` | peer methodology — produces inputs or consumes outputs |
| `pro/product/customer-success-basics` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/churn-cohort-analysis.md.j2` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/churn-cohort-analysis.md` | Filled artefact skeleton conforming to 02-output-contract.xml Generated from `templates/churn-cohort-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/churn-cohort-analysis.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in version exercised by scripts/validate-churn-cohort-analysis.py --self-test |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-churn-cohort-analysis.py --self-test Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-churn-cohort-analysis.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/product/product-analytics`
- peer methodology: `pro/product/customer-success-basics`
- external: https://www.lennyrachitsky.com/p/churn-benchmarks (Lenny benchmarks); https://www.profitwell.com/recur/all/churn

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/churn-cohort-analysis.schema.json`

```json
{
  "__faion_header__": {
    "purpose": "JSON Schema for churn-cohort-analysis",
    "consumes": "validated against artefacts produced by the methodology",
    "produces": "schema document for validator script",
    "depends_on": "content/02-output-contract.xml",
    "token_budget_impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/churn-cohort-analysis.json",
  "type": "object",
  "required": ["artefact_id", "owner", "decision", "version", "last_reviewed", "inputs_used"],
  "properties": {
    "artefact_id": { "type": "string", "pattern": "^[a-z][a-z0-9-]+$" },
    "owner": { "type": "string", "minLength": 2 },
    "decision": { "type": "string", "minLength": 2 },
    "rationale": { "type": "string" },
    "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "last_reviewed": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "inputs_used": { "type": "array", "items": { "type": "string" }, "minItems": 1 }
  }
}
```
