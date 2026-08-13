# Freelance Weekly Invoice Cadence

## Summary

**One-sentence:** Weekly invoice + automated reminder + escalation ladder routine for solo freelancers; produces an auditable per-week invoice batch artefact with reminder/escalation steps.

**One-paragraph:** Freelance Weekly Invoice Cadence defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 5 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Solo freelancer with 2-8 active retainers and recurring scope.
- Engagements where late payment (>30d) is the dominant cash-flow risk.
- Operator needs an audit trail of when reminders fired and which escalations are due.
- Workflow is monitored by exactly one human owner (not a team).

## Applies If (ALL must hold)

- At least one active client invoiced on a weekly or sub-monthly cadence.
- Operator has write access to the billing tool (Stripe / Wise / ledger).
- A named consumer reads the cadence artefact (the operator themselves counts).
- Prior week's invoice batch is accessible for delta + carry-forward.

## Skip If (ANY kills it)

- One-time fixed-price gig with a single invoice — overhead does not pay back.
- Client pays via auto-debit / subscription and no reminder ladder is needed.
- Operator cannot legally invoice (entity setup pending).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `freelance-weekly-invoice-cadence_template_fill` | haiku | Bounded template fill, no judgement. |
| `freelance-weekly-invoice-cadence_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `freelance-weekly-invoice-cadence_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the weekly invoice batch artefact. |
| `templates/invoice-row.md` | Per-client invoice row skeleton with evidence + reason fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-weekly-invoice-cadence.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/freelance-weekly-invoice-cadence.json",
  "type": "object",
  "required": [
    "batch_id",
    "week_ending",
    "rows",
    "reminders_scheduled",
    "escalations_due",
    "status"
  ],
  "properties": {
    "batch_id": {
      "type": "string",
      "pattern": "^fwic-\\d{4}-W\\d{2}$"
    },
    "week_ending": {
      "type": "string",
      "format": "date"
    },
    "rows": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "client_id",
          "amount",
          "currency",
          "evidence"
        ]
      }
    },
    "reminders_scheduled": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "invoice_id",
          "fires_on",
          "rung"
        ],
        "properties": {
          "rung": {
            "enum": [
              "nudge",
              "follow-up",
              "pause-notice"
            ]
          }
        }
      }
    },
    "escalations_due": {
      "type": "array"
    },
    "status": {
      "enum": [
        "draft",
        "ready_for_review",
        "approved_to_send",
        "sent",
        "archived"
      ]
    }
  }
}
```
