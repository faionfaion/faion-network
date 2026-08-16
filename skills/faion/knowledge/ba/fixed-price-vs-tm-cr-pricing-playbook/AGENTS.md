# Fixed-Price vs T&M Change-Request Pricing Playbook

## Summary

**One-sentence:** Produces a change-request playbook for P4 outsource BAs at the BA/procurement boundary: classify each CR by contract type (fixed-price vs T&M), apply absorb / negotiate-addendum / scope-swap decisions, and price residual risk explicitly.

**Ефективно для:** P4 outsource BAs handling change requests under fixed-price + T&M contracts; commercial leads defending CR pricing; PMs negotiating scope swaps without margin leak.

**One-paragraph:** This methodology pins the recurring decision around "fixed-price-vs-tm-cr-pricing-playbook" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Engagement runs under fixed-price OR T&M contract.
- Change requests arrive after baseline scope agreed.
- BA owns the CR pricing recommendation.
- Owner exists for the playbook step.

## Skip If (ANY kills it)

- Engagement is internal product team — no contract boundary.
- Vendor handles all CR pricing — link out.
- Pilot with no signed contract yet.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Baseline scope + price | spec + commercial doc | commercial |
| Change request (CR) text | Markdown / ticket | client / PM |
| Historical CR outcomes (absorbed / addendum / swap) | spreadsheet | commercial |
| Margin and contingency status | spreadsheet | finance |
| Playbook owner | handle / email | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[fixed-price-risk-loading-model]]` | risk loading model produced the baseline buffer |

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
| `draft_cr_classification` | haiku | Template fill from CR text. |
| `synthesize_decision` | sonnet | Absorb vs addendum vs swap judgment. |
| `escalate_margin_breach` | opus | Cross-CR margin compounding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixed-price-vs-tm-cr-pricing-playbook.json` | JSON Schema for the Fixed-Price vs T&M Change-Request Pricing Playbook output contract |
| `templates/fixed-price-vs-tm-cr-pricing-playbook.md.j2` | Markdown skeleton with the required fields |
| `templates/fixed-price-vs-tm-cr-pricing-playbook.md` | Markdown skeleton with the required fields Generated from `templates/fixed-price-vs-tm-cr-pricing-playbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a fixed-price-vs-tm-cr-pricing-playbook record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a fixed-price-vs-tm-cr-pricing-playbook record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-price-vs-tm-cr-pricing-playbook.py` | Enforce the Fixed-Price vs T&M Change-Request Pricing Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fixed-price-risk-loading-model]] — upstream risk-loading model.
- [[compliance-traceability-pack]] — when CR touches compliance scope.
- [[ai-enabled-business-analysis]] — parent BA methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fixed-price-vs-tm-cr-pricing-playbook.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/fixed-price-vs-tm-cr-pricing-playbook.json",
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
      "pattern": "^fpcr-[a-z0-9-]+$"
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
