# Foreign Client Kickoff Checklist

## Summary

**One-sentence:** 30-item kickoff checklist for 2-week foreign-client onboarding: stakeholder map, comms cadence, decision-makers, holiday calendar, payment terms, IP regime, escalation route.

**One-paragraph:** Foreign Client Kickoff Checklist delivers a defensible checklist artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource agency, що запускає 6-12-тиж проект з новим foreign-client.
- Solo фрілансер, що приймає US/EU клієнта і не може дозволити missing-info ризик.
- Founder-PM на першому international engagement: timezone, holidays, IP regime, payment cycle.
- PMO template owner, що стандартизує kickoff across 5-15 active engagements.

## Applies If (ALL must hold)

- a new foreign-client engagement is starting and a kickoff window of 1-2 weeks exists
- the engagement is large enough that kickoff overhead is justified (≥ 4 weeks of work)
- the PM has authority to gather + record kickoff inputs
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- engagement is under 2 weeks — full kickoff checklist overhead unjustified
- this is the third+ engagement with the same client — reuse prior checklist, skip from-scratch run
- kickoff was already done informally and recorded elsewhere — do not duplicate

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
| `content/02-output-contract.xml` | essential | JSON Schema for the checklist + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-foreign_client_kickoff_checklist` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/foreign-client-kickoff-checklist.md` | checklist skeleton with required fields + 5-line header |
| `templates/foreign-client-kickoff-checklist.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-foreign-client-kickoff-checklist.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[foreign-client-etiquette-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/foreign-client-kickoff-checklist.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/foreign-client-kickoff-checklist.json",
  "title": "Foreign Client Kickoff Checklist",
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
