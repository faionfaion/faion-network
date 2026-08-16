# Cross Timezone Standup Rotation

## Summary

**One-sentence:** Rotation schedule artefact for distributed standups: anchored handoff windows, named owners per timezone, 90-day refresh cadence, citation-traceable rationale.

**One-paragraph:** Cross Timezone Standup Rotation delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Distributed дев-команда з вікнами перекриття <3 годин і потребою в передачі owner-of-day.
- Outsource P4 (EU+LATAM/APAC+NA) — потрібен auditable handoff артефакт для клієнта.
- P6 multi-squad всередині однієї компанії, де standup переходить між клітинками.
- Команда, що готується до 24/7 on-call ротації і репетирує handoff-discipline.

## Applies If (ALL must hold)

- the team spans 2+ timezones with overlap window under 3 hours
- daily ceremony exists or is being established (standup, demo, async-update)
- downstream consumer reads the rotation artefact (ops, eng leads, client PM)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- single timezone or co-located team — rotation overhead unjustified
- ceremony itself is being deprecated — fix that first
- team size below 4 — informal handoff is cheaper
- regulatory rota schedule already mandated by HR or labour law

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-cross_timezone_standup_rotation` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/cross-timezone-standup-rotation.md.j2` | spec skeleton with required fields + 5-line header |
| `templates/cross-timezone-standup-rotation.md` | spec skeleton with required fields + 5-line header Generated from `templates/cross-timezone-standup-rotation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/cross-timezone-standup-rotation.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md.j2` | minimum viable filled-in example |
| `templates/_smoke-test.md` | minimum viable filled-in example Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-timezone-standup-rotation.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[follow-the-sun-handoff-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cross-timezone-standup-rotation.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/cross-timezone-standup-rotation.json",
  "title": "Cross Timezone Standup Rotation",
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
  "additionalProperties": false,
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]+$",
      "minLength": 3,
      "maxLength": 80
    },
    "owner": {
      "type": "string",
      "minLength": 2,
      "maxLength": 80
    },
    "decision": {
      "type": "string",
      "minLength": 4,
      "maxLength": 4000
    },
    "rationale": {
      "type": "string",
      "minLength": 40,
      "maxLength": 4000
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
            "type": "string",
            "minLength": 2
          },
          "source": {
            "type": "string",
            "minLength": 4
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
    "status": {
      "enum": [
        "draft",
        "pending",
        "active",
        "deprecated"
      ]
    },
    "notes": {
      "type": "string",
      "maxLength": 2000
    }
  }
}
```
