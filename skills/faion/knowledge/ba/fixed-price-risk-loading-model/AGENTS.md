# Fixed-Price Risk Loading Model

## Summary

**One-sentence:** Produces a fixed-price risk loading model: risk-register-to-buffer translation, contingency tiers, hidden-cost classes, and a defensible bid number with explicit risk-pricing reasoning per category.

**Ефективно для:** BAs / sales engineers pricing fixed-price engagements; commercial leads defending bid margins to procurement; partners pricing P4 outsource engagements.

**One-paragraph:** This methodology pins the recurring decision around "fixed-price-risk-loading-model" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Engagement is fixed-price (not T&M).
- Risk register exists OR can be built.
- Bid number is defensible against procurement.
- Owner exists for the model.

## Skip If (ANY kills it)

- Engagement is T&M — loading model does not apply.
- Bid is volume-only with no risk premium negotiated.
- Standardised price-list product with no scope-risk variance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Risk register (likelihood × impact) | CSV | BA / delivery |
| Historical loading ratios | spreadsheet | finance |
| Engagement scope | Markdown spec | BA |
| Bid owner | handle / email | commercial |
| Procurement constraints | Markdown | commercial |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[fixed-price-vs-tm-cr-pricing-playbook]]` | change-request flow runs after bid signed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_loading_table` | haiku | Mechanical template fill. |
| `synthesize_buffer` | sonnet | Per-class buffer judgment. |
| `escalate_margin` | opus | Cross-class margin decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixed-price-risk-loading-model.json` | JSON Schema for the Fixed-Price Risk Loading Model output contract |
| `templates/fixed-price-risk-loading-model.md.j2` | Markdown skeleton with the required fields |
| `templates/fixed-price-risk-loading-model.md` | Markdown skeleton with the required fields Generated from `templates/fixed-price-risk-loading-model.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a fixed-price-risk-loading-model record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a fixed-price-risk-loading-model record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-price-risk-loading-model.py` | Enforce the Fixed-Price Risk Loading Model output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fixed-price-vs-tm-cr-pricing-playbook]] — adjacent change-request playbook.
- [[compliance-traceability-pack]] — when risk is regulatory.
- [[ai-enabled-business-analysis]] — parent BA methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fixed-price-risk-loading-model.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/fixed-price-risk-loading-model.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^fprl-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
