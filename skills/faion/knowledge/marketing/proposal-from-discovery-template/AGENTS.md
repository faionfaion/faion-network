# Proposal From Discovery Template

## Summary

**One-sentence:** A one-page three-option proposal template fed directly from discovery-call notes, with fixed sections, evidence anchors, a named owner, and a published outcome-review cadence.

**One-paragraph:** Solo technical freelancers lose inbound deals on slow proposal turnaround. The upstream `discovery-call-structure` methodology produces verbatim pain notes but stops there; this methodology converts those notes into a committed one-page artefact with three offers (light / standard / outcome-based), each anchored to an evidence link, owned by a named person, and reviewed against close-rate at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored proposal document the freelancer can send within the same client-cycle as the discovery call.

**Ефективно для:**

- Одного фрілансера, що закриває inbound-ліди в межах одного циклу спілкування.
- Конвертації нотаток discovery-call у три ціновані опції на одну сторінку.
- Регулярного outcome-review: чи проп з шаблону справді закриває угоди частіше.
- Командного контролю якості — фіксована форма + іменований власник + версія.

## Applies If (ALL must hold)

- The freelancer runs the inbound-to-signed-retainer loop on a recurring cadence (≥1/month).
- Upstream `discovery-call-structure` notes (verbatim pain + budget signal) are available.
- The freelancer owns the artefact (or escalates ownership to a named person).
- The team has a version-controlled or wiki-style space where the artefact lives.

## Skip If (ANY kills it)

- One-off deal with no recurrence — write a single doc, not a versioned artefact.
- Fewer than 3 inbound proposals per year — review cadence costs more than it returns.
- Procurement-led RFP that mandates a different shape — fill the RFP's template instead.
- No named owner is available — defer until ownership is resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Discovery-call notes | Markdown / transcript | upstream `discovery-call-structure` |
| Rate card | JSON / sheet | freelancer's pricing doc |
| Three offer scaffolds | YAML | this methodology's `templates/skeleton.md` |
| Repository / wiki path | URL | team knowledge space |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/rate-raise-conversation-script` | Anchors pricing language for the outcome-based option. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fixed shape, evidence anchors, named owner, version+last_reviewed, outcome review | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: notes → scaffold → fill → review → commit | ~800 |
| `content/05-examples.xml` | essential | One worked proposal end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Mechanical fill from header + section list. |
| `populate-evidence-fields` | sonnet | Per-section judgment: pick the right evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change close-rate? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root. |
| `templates/proposal-from-discovery-template.json` | JSON schema for the output contract. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/proposal-from-discovery-template.md.j2` | canonical markdown skeleton for the Proposal From Discovery Template artefact |
| `templates/proposal-from-discovery-template.md` | canonical markdown skeleton for the Proposal From Discovery Template artefact Generated from `templates/proposal-from-discovery-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-proposal-from-discovery-template.py` | Validate a filled artefact against the schema in `02-output-contract.xml`. | Pre-commit; before sending to client. |

## Related

- [[rate-raise-conversation-script]]
- [[single-page-case-study-generation]]
- [[retainer-pricing-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (inbound count, has_discovery_notes, named_owner_present, recurrence_per_year) to a rule from `01-core-rules.xml`. Use it whenever an inbound lead lands and you have to decide between filling the proposal template, deferring (no owner), or writing a one-off email.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/header.yaml`

```yaml
version: 1.0.0          # semver
owner: <named-human>    # not "team", not "we"
last_reviewed: 2026-05-23  # ISO date; ≤90 days old at use time
client: <client-name>   # ≥2 chars
title: <one-line>       # 8-120 chars
```

### `templates/proposal-from-discovery-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/proposal-from-discovery-template.json",
  "type": "object",
  "required": [
    "header",
    "discovery_inputs",
    "options",
    "actions"
  ],
  "properties": {
    "header": {
      "type": "object",
      "required": [
        "version",
        "owner",
        "last_reviewed",
        "client",
        "title"
      ],
      "properties": {
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "owner": {
          "type": "string",
          "minLength": 3
        },
        "last_reviewed": {
          "type": "string",
          "format": "date"
        },
        "client": {
          "type": "string",
          "minLength": 2
        },
        "title": {
          "type": "string",
          "minLength": 8,
          "maxLength": 120
        }
      }
    },
    "discovery_inputs": {
      "type": "object",
      "required": [
        "pain",
        "budget_signal",
        "evidence_links"
      ],
      "properties": {
        "pain": {
          "type": "string",
          "minLength": 30
        },
        "budget_signal": {
          "type": "string"
        },
        "evidence_links": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        }
      }
    },
    "options": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": [
          "name",
          "scope",
          "price",
          "duration_weeks"
        ],
        "properties": {
          "name": {
            "enum": [
              "light",
              "standard",
              "outcome-based"
            ]
          },
          "scope": {
            "type": "string",
            "minLength": 20
          },
          "price": {
            "type": "number",
            "minimum": 0
          },
          "duration_weeks": {
            "type": "integer",
            "minimum": 1,
            "maximum": 52
          }
        }
      }
    },
    "actions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "owner",
          "due_date",
          "action"
        ],
        "properties": {
          "owner": {
            "type": "string"
          },
          "due_date": {
            "type": "string",
            "format": "date"
          },
          "action": {
            "type": "string"
          }
        }
      }
    }
  }
}
```
