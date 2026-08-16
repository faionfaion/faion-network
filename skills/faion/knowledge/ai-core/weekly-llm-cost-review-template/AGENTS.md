# Weekly LLM Cost Review Template

## Summary

**One-sentence:** Produces a weekly LLM cost + token-budget review report: spend by surface / model / provider, top drivers, deviation from forecast, action items with owners and due-dates.

**Ефективно для:** ML engineers + finance running a weekly LLM spend review; PMs tracking model-cost-to-revenue ratio; FinOps embedding LLM into the cloud-cost cadence.

**One-paragraph:** This methodology pins the recurring decision around "weekly-llm-cost-review-template" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Team has ≥3 weeks of LLM cost telemetry segmented by surface + model.
- Weekly cadence exists or is being introduced.
- Owner exists for cost decisions.
- Forecast (target or budget) exists or is being introduced.

## Skip If (ANY kills it)

- Team has <2 weeks of telemetry — bootstrap that first.
- Spend below review-overhead threshold (<$500/mo).
- Single-tenant prototype with no production traffic.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Weekly cost telemetry (last 4 weeks) | CSV / Parquet | FinOps |
| Surface / model / provider taxonomy | Markdown | platform |
| Forecast / budget | spreadsheet | finance |
| Owner for action items | handle / email | team roster |
| Previous week's action-item log | Markdown | review owner |

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
| `draft_report_grid` | haiku | Template fill from telemetry. |
| `synthesize_drivers` | sonnet | Per-surface root-cause for top drivers. |
| `escalate_runaway` | opus | Cross-surface budget breach decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-llm-cost-review-template.json` | JSON Schema for the Weekly LLM Cost Review Template output contract |
| `templates/weekly-llm-cost-review-template.md.j2` | Markdown skeleton with the required fields |
| `templates/weekly-llm-cost-review-template.md` | Markdown skeleton with the required fields Generated from `templates/weekly-llm-cost-review-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a weekly-llm-cost-review-template record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a weekly-llm-cost-review-template record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-llm-cost-review-template.py` | Enforce the Weekly LLM Cost Review Template output contract | After subagent returns, before downstream consumer reads |

## Related

- [[fine-tune-vs-prompt-decision-tree]] — adjacent decision when costs blow.
- [[vector-db-tuning-runbook]] — adjacent when cost driver is retrieval.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/weekly-llm-cost-review-template.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/weekly-llm-cost-review-template.json",
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
      "pattern": "^wlcr-[a-z0-9-]+$"
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
