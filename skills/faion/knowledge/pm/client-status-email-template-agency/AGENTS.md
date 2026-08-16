# Client Status Email Template Agency

## Summary

**One-sentence:** Generates a weekly client status email — progress, risks, decisions needed, asks, next week plan — in a 5-section template.

**One-paragraph:** Client Status Email Template Agency addresses the gap identified by the `p5-micro-agency-founder/Weekly client status email batch` playbook: Status emails meander or get skipped; clients then ask 'where are we'. A template forces five sections every week and a clear decisions-needed block. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `spec` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Структурований spec-артефакт, що читається людиною і парситься машиною.
- Типізовані поля з обов'язковим джерелом — жодного 'team' / 'we' як власника.
- Версіонована, ревью‑датована форма — артефакт не стає stale без сигналу.
- Контрактний валідатор blocks вихід, який не задовольняє схему.

## Applies If (ALL must hold)

- Task is an instance of `p5-micro-agency-founder/Weekly client status email batch` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `p5-micro-agency-founder/Weekly client status email batch` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `spec` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example producing a valid `spec` artefact | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-spec` | sonnet | Per-instance judgment over bounded inputs to fill the `spec` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-status-email-template-agency.json` | JSON Schema (draft-07) for the Client Status Email Template Agency output contract |
| `templates/client-status-email-template-agency.md.j2` | Markdown skeleton with the required fields for the Client Status Email Template Agency artefact |
| `templates/client-status-email-template-agency.md` | Markdown skeleton with the required fields for the Client Status Email Template Agency artefact Generated from `templates/client-status-email-template-agency.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/client-status-email-template-agency.example.json` | Worked filled-in example of a valid Client Status Email Template Agency artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-status-email-template-agency.py` | Enforce the Client Status Email Template Agency output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `p5-micro-agency-founder/Weekly client status email batch`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/client-status-email-template-agency.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/pm/client-status-email-template-agency.json",
  "title": "Client Status Email Template Agency",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "spec_body"
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
    "spec_body": {
      "type": "string",
      "minLength": 40
    }
  }
}
```

### `templates/client-status-email-template-agency.example.json`

```json
{
  "artefact_id": "client-status-email-template-agency-2026-05-23-acme",
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
  "spec_body": "1. Scope: in / out of scope for this engagement. 2. Owner: ruslan@faion.net. 3. Cadence: weekly. 4. Acceptance: signed by client lead."
}
```
