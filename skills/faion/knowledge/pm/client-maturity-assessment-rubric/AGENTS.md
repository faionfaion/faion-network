# Client Maturity Assessment Rubric

## Summary

**One-sentence:** Generates a maturity score across decision velocity, tech literacy, ops readiness and political alignment — used to size cadence and risk buffers.

**One-paragraph:** Client Maturity Assessment Rubric addresses the gap identified by the `role-project-manager/Client onboarding into our delivery cadence (two weeks)` playbook: Treating every client identically over-engineers the low-maturity ones and under-serves the high-maturity ones. A maturity rubric calibrates cadence and buffers. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `rubric` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Зважений scorecard з явними ваговими коефіцієнтами та порогом pass / fail.
- Кожен вимір прив'язаний до evidence, а не до vibes — ревью‑friendly.
- Артефакт несе версію + last_reviewed; стейл flagged on read.
- Контрактний валідатор перевіряє діапазони + threshold + наявність owner.

## Applies If (ALL must hold)

- Task is an instance of `role-project-manager/Client onboarding into our delivery cadence (two weeks)` OR a closely-adjacent variant in the same engagement shape.
- Operator has all artefacts named in Prerequisites available before starting.
- Output will be consumed by a downstream agent or human reviewer (not discarded after one read).
- Tier == pro or higher (gating enforced by `tier-manifest.json`).

## Skip If (ANY kills it)

- Team already maintains a working artefact for this gap — update it, do not duplicate.
- Change being decided is a greenfield prototype with no production users or paying client.
- Regulatory / compliance context overrides in-methodology guidance — defer to legal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent context for the `role-project-manager/Client onboarding into our delivery cadence (two weeks)` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `rubric` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-rubric` | sonnet | Per-instance judgment over bounded inputs to fill the `rubric` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-maturity-assessment-rubric.json` | JSON Schema (draft-07) for the Client Maturity Assessment Rubric output contract |
| `templates/client-maturity-assessment-rubric.md.j2` | Markdown skeleton with the required fields for the Client Maturity Assessment Rubric artefact |
| `templates/client-maturity-assessment-rubric.md` | Markdown skeleton with the required fields for the Client Maturity Assessment Rubric artefact Generated from `templates/client-maturity-assessment-rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/client-maturity-assessment-rubric.example.json` | Worked filled-in example of a valid Client Maturity Assessment Rubric artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-maturity-assessment-rubric.py` | Enforce the Client Maturity Assessment Rubric output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-project-manager/Client onboarding into our delivery cadence (two weeks)`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/client-maturity-assessment-rubric.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/pm/client-maturity-assessment-rubric.json",
  "title": "Client Maturity Assessment Rubric",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "dimensions",
    "threshold"
  ],
  "additionalProperties": true,
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "not": {
        "enum": [
          "team",
          "we",
          "us",
          "engineering"
        ]
      }
    },
    "decision": {
      "type": "string",
      "minLength": 1
    },
    "rationale": {
      "type": "string",
      "minLength": 40
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
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "dimensions": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "name",
          "weight",
          "score"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "weight": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "score": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "evidence": {
            "type": "string"
          }
        }
      }
    },
    "threshold": {
      "type": "number",
      "minimum": 0,
      "maximum": 5
    }
  }
}
```

### `templates/client-maturity-assessment-rubric.example.json`

```json
{
  "artefact_id": "client-maturity-assessment-rubric-2026-05-23-acme",
  "owner": "ruslan@faion.net",
  "decision": "Proceed with the agreed plan as captured in the linked inputs.",
  "rationale": "Decision rests on the latest engagement notes (notes-2026-05-22) and the prior baseline (baseline-2026-05-15); both inputs corroborate the same direction without contradicting constraints.",
  "inputs_used": [
    {
      "name": "notes-2026-05-22",
      "source": "wiki://pm/notes/2026-05-22.md"
    },
    {
      "name": "baseline-2026-05-15",
      "source": "repo://artefacts/baseline-2026-05-15.json"
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "dimensions": [
    {
      "name": "margin",
      "weight": 0.35,
      "score": 3.5,
      "evidence": "Modelled margin 28% per finance sheet 2026-Q2."
    },
    {
      "name": "fit",
      "weight": 0.25,
      "score": 4.0,
      "evidence": "Stack overlaps with two prior wins (proj-A, proj-B)."
    },
    {
      "name": "compliance-burden",
      "weight": 0.2,
      "score": 2.5,
      "evidence": "GDPR + HIPAA-lite per RFP section 7."
    },
    {
      "name": "ai-leverage",
      "weight": 0.2,
      "score": 4.5,
      "evidence": "70% of LOE classified as agentable per audit-2026-05-20."
    }
  ],
  "threshold": 3.0
}
```
