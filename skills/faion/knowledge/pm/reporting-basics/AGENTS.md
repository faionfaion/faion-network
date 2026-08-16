# Reporting Basics

## Summary

**One-sentence:** Weekly / monthly project reporting basics: actionable KPI selection, dashboard wireframe, narrative summary, escalation flags, distribution list.

**One-paragraph:** Reporting Basics defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- PM building the first reporting cadence for a new program.
- Coaches helping a team move from 'status email' to a measurable dashboard.
- Stakeholders who want a uniform weekly snapshot they can scan in 60 seconds.
- PMOs standardising reporting structure across portfolios.

## Applies If (ALL must hold)

- Team has at least 4 weeks of measurable activity (issues, sprints, releases).
- A reporting tool (dashboard / spreadsheet / wiki) is available.
- Stakeholders agree to read the report (named distribution list).
- Author has authority to publish on the cadence.

## Skip If (ANY kills it)

- Stakeholders ignore reports — fix the engagement first.
- No measurable activity yet — reporting is theatre.
- Existing reporting is working — don't add a parallel cadence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `reporting-basics_template_fill` | haiku | Bounded template fill, no judgement. |
| `reporting-basics_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `reporting-basics_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the weekly/monthly report artefact. |
| `templates/report.md.j2` | Markdown skeleton for the report with KPI table + narrative + escalation flags. |
| `templates/report.md` | Markdown skeleton for the report with KPI table + narrative + escalation flags. Generated from `templates/report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reporting-basics.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

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
  "$id": "https://faion.net/schemas/reporting-basics.json",
  "type": "object",
  "required": [
    "report_id",
    "cadence",
    "kpis",
    "narrative",
    "escalation_flags",
    "distribution_list"
  ],
  "properties": {
    "report_id": {
      "type": "string"
    },
    "cadence": {
      "enum": [
        "weekly",
        "biweekly",
        "monthly"
      ]
    },
    "kpis": {
      "type": "array",
      "minItems": 3,
      "items": {
        "type": "object",
        "required": [
          "name",
          "value",
          "threshold",
          "source"
        ]
      }
    },
    "narrative": {
      "type": "string",
      "minLength": 80,
      "maxLength": 600
    },
    "escalation_flags": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "kpi",
          "owner",
          "proposed_action"
        ]
      }
    },
    "distribution_list": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    }
  }
}
```
