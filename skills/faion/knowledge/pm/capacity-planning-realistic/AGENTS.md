# Capacity Planning Realistic

## Summary

**One-sentence:** Generates a realistic per-sprint capacity plan that nets out PTO, on-call, meetings, support and ad-hoc — usable budget, not gross headcount.

**One-paragraph:** Capacity Planning Realistic addresses the gap identified by the `role-project-manager/AI-assisted sprint planning with capacity reality-check` playbook: Naive capacity = headcount × hours over-promises every sprint. Realistic capacity nets out PTO, on-call, meetings, support tax, and ad-hoc interruptions. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `spec` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Структурований spec-артефакт, що читається людиною і парситься машиною.
- Типізовані поля з обов'язковим джерелом — жодного 'team' / 'we' як власника.
- Версіонована, ревью‑датована форма — артефакт не стає stale без сигналу.
- Контрактний валідатор blocks вихід, який не задовольняє схему.

## Applies If (ALL must hold)

- Task is an instance of `role-project-manager/AI-assisted sprint planning with capacity reality-check` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `role-project-manager/AI-assisted sprint planning with capacity reality-check` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `spec` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
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
| `templates/capacity-planning-realistic.json` | JSON Schema (draft-07) for the Capacity Planning Realistic output contract |
| `templates/capacity-planning-realistic.md.j2` | Markdown skeleton with the required fields for the Capacity Planning Realistic artefact |
| `templates/capacity-planning-realistic.md` | Markdown skeleton with the required fields for the Capacity Planning Realistic artefact Generated from `templates/capacity-planning-realistic.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/capacity-planning-realistic.example.json` | Worked filled-in example of a valid Capacity Planning Realistic artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-planning-realistic.py` | Enforce the Capacity Planning Realistic output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-project-manager/AI-assisted sprint planning with capacity reality-check`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capacity-planning-realistic.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/pm/capacity-planning-realistic.json",
  "title": "Capacity Planning Realistic",
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

### `templates/capacity-planning-realistic.example.json`

```json
{
  "artefact_id": "capacity-planning-realistic-2026-05-23-acme",
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
