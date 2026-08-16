# Client Handover Master Checklist

## Summary

**One-sentence:** Generates an end-of-engagement handover checklist — code, infra, credentials, docs, runbooks, on-call rotation, knowledge transfer sessions with sign-offs.

**One-paragraph:** Client Handover Master Checklist addresses the gap identified by the `p4-outsource-specialist/Handover to client in-house team (3 weeks)` playbook: Handovers drop balls (credentials, runbooks, on-call) when the vendor exits. A master checklist forces each artefact to a named receiver with a signed acceptance. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `checklist` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Бінарний checklist, де кожен пункт має owner і `done_by` дату.
- Sign-off field — артефакт неможливо позначити complete без named approver.
- Версіонована форма + last_reviewed; redo at next cycle.
- Контрактний валідатор перевіряє, що всі обов'язкові пункти заповнені.

## Applies If (ALL must hold)

- Task is an instance of `p4-outsource-specialist/Handover to client in-house team (3 weeks)` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `p4-outsource-specialist/Handover to client in-house team (3 weeks)` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `checklist` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-checklist` | sonnet | Per-instance judgment over bounded inputs to fill the `checklist` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-handover-master-checklist.json` | JSON Schema (draft-07) for the Client Handover Master Checklist output contract |
| `templates/client-handover-master-checklist.md.j2` | Markdown skeleton with the required fields for the Client Handover Master Checklist artefact |
| `templates/client-handover-master-checklist.md` | Markdown skeleton with the required fields for the Client Handover Master Checklist artefact Generated from `templates/client-handover-master-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/client-handover-master-checklist.example.json` | Worked filled-in example of a valid Client Handover Master Checklist artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-handover-master-checklist.py` | Enforce the Client Handover Master Checklist output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `p4-outsource-specialist/Handover to client in-house team (3 weeks)`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/client-handover-master-checklist.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/pm/client-handover-master-checklist.json",
  "title": "Client Handover Master Checklist",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "items"
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
    "items": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "text",
          "done",
          "owner"
        ],
        "properties": {
          "text": {
            "type": "string"
          },
          "done": {
            "type": "boolean"
          },
          "owner": {
            "type": "string"
          },
          "due_by": {
            "type": "string",
            "format": "date"
          }
        }
      }
    }
  }
}
```

### `templates/client-handover-master-checklist.example.json`

```json
{
  "artefact_id": "client-handover-master-checklist-2026-05-23-acme",
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
  "items": [
    {
      "text": "Comms draft reviewed by client lead",
      "done": true,
      "owner": "ruslan@faion.net",
      "due_by": "2026-05-22"
    },
    {
      "text": "Billing provider toggle staged",
      "done": false,
      "owner": "ops-lead@faion.net",
      "due_by": "2026-05-30"
    },
    {
      "text": "Finance reconciliation script tested",
      "done": false,
      "owner": "finance@faion.net",
      "due_by": "2026-05-29"
    }
  ]
}
```
