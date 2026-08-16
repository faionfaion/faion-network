# Capacity vs Ask Balancer

## Summary

**One-sentence:** Generates a quarter-level decision record that reconciles requested scope against realistic capacity — accepted, deferred, dropped lines with rationale.

**One-paragraph:** Capacity vs Ask Balancer addresses the gap identified by the `role-product-manager/Quarter planning + OKR cascade` playbook: OKR cascades collect more asks than capacity allows. Without an explicit balancer, low-leverage asks crowd out the high-leverage ones by default. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned `decision-record` artefact carrying a named accountable owner, input citations, and a review date — downstream agents and human reviewers consume it without re-deriving the rationale.

**Ефективно для:**

- Decision record з options, рішенням, rationale і default-if-silent.
- Іменований власник — жодного 'team' / 'we' як вирішувача.
- Зв'язана з input-артефактами по path/URL, без вільної прози без цитувань.
- Версіонована; bumping required при матеріальній зміні рішення.

## Applies If (ALL must hold)

- Task is an instance of `role-product-manager/Quarter planning + OKR cascade` OR a closely-adjacent variant in the same engagement shape.
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
| Recent context for the `role-product-manager/Quarter planning + OKR cascade` task (last 30 days) | Markdown / chat log | engagement notes |
| Write-access to the artefact store | repo / wiki / decision log | infra |
| Named accountable owner (handle / email / role) | string | engagement RACI |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-input-citations | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for `decision-record` shape + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate per step | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template-fill of inputs from named sources; bounded transformation. |
| `synthesize-decision-record` | sonnet | Per-instance judgment over bounded inputs to fill the `decision-record` shape. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (regulatory / large €). |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-vs-ask-balancer.json` | JSON Schema (draft-07) for the Capacity vs Ask Balancer output contract |
| `templates/capacity-vs-ask-balancer.md.j2` | Markdown skeleton with the required fields for the Capacity vs Ask Balancer artefact |
| `templates/capacity-vs-ask-balancer.md` | Markdown skeleton with the required fields for the Capacity vs Ask Balancer artefact Generated from `templates/capacity-vs-ask-balancer.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/capacity-vs-ask-balancer.example.json` | Worked filled-in example of a valid Capacity vs Ask Balancer artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-vs-ask-balancer.py` | Enforce the Capacity vs Ask Balancer output contract against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-pricing-rubric]]
- [[client-status-email-template-agency]]
- upstream playbook: `role-product-manager/Quarter planning + OKR cascade`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, owner named yes/no, decision materiality) to a concrete action, with each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, route to a sibling methodology, or skip entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capacity-vs-ask-balancer.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/pm/capacity-vs-ask-balancer.json",
  "title": "Capacity vs Ask Balancer",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "options",
    "default_if_silent"
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
    "options": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "name",
          "pros",
          "cons"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "pros": {
            "type": "string"
          },
          "cons": {
            "type": "string"
          }
        }
      }
    },
    "default_if_silent": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

### `templates/capacity-vs-ask-balancer.example.json`

```json
{
  "artefact_id": "capacity-vs-ask-balancer-2026-05-23-acme",
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
  "options": [
    {
      "name": "option-a-defer",
      "pros": "Keeps margin stable.",
      "cons": "Slips OKR-2."
    },
    {
      "name": "option-b-ship-narrow",
      "pros": "Hits OKR-2 partially.",
      "cons": "Adds 1.5w to roadmap."
    }
  ],
  "default_if_silent": "option-a-defer"
}
```
