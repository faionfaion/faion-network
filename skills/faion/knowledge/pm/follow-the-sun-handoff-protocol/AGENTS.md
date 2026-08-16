# Follow-The-Sun Handoff Protocol

## Summary

**One-sentence:** Async-cross-timezone delivery cadence: 24-hour rotation with anchored handoff windows, baton artefact (state + blockers + next-N tasks), owner-of-day, baton SLA.

**One-paragraph:** Follow-The-Sun Handoff Protocol delivers a defensible playbook-step artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource agency: EU + LATAM або APAC + NA, 24-hour follow-the-sun рішення.
- Distressed-project rescue, що додає second-shift команду до існуючої первинної.
- Open-source maintainer team з global contributors і потребою owner-of-day розкладу.
- Founder-PM з 2 розкиданими timezones, що тестує модель перед масштабуванням.

## Applies If (ALL must hold)

- team spans at least two non-overlapping timezones with under 2 hours overlap
- work is decomposable into tasks each closable within one timezone's working day
- single product / repo / workstream — not parallel independent streams
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- co-located or single-timezone team — protocol overhead unjustified
- tasks routinely span multiple days and cannot be checkpointed at handoff — fix decomposition first
- team has fewer than one engineer per timezone — protocol needs at least one named owner per zone

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the playbook-step + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-follow_the_sun_handoff_protocol` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/follow-the-sun-handoff-protocol.md.j2` | playbook-step skeleton with required fields + 5-line header |
| `templates/follow-the-sun-handoff-protocol.md` | playbook-step skeleton with required fields + 5-line header Generated from `templates/follow-the-sun-handoff-protocol.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/follow-the-sun-handoff-protocol.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md.j2` | minimum viable filled-in example |
| `templates/_smoke-test.md` | minimum viable filled-in example Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-follow-the-sun-handoff-protocol.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[cross-timezone-standup-rotation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/follow-the-sun-handoff-protocol.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/follow-the-sun-handoff-protocol.json",
  "title": "Follow-The-Sun Handoff Protocol",
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
