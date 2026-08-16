# Notion PM

## Summary

**One-sentence:** Solo / small-team Notion PM workspace: Projects + Tasks + Sprints databases with relations + rollups; single tasks DB across sprints; ≤20 properties.

**One-paragraph:** Pins the Notion PM baseline: one Tasks database with Sprint as a relation field, one Projects database with rollups, four canonical views per DB, native automations bounded to property triggers, external automation via n8n for time-triggered jobs. Output is a versioned setup spec covering schemas + views + automation + API gotchas.

**Ефективно для:**

- Solo founder or 2-10-person team using Notion as PM + docs + wiki. Avoids the per-sprint-database trap and the 60-property bloat; sets up the workspace once for the year.

## Applies If (ALL must hold)

- Small agile team (2-10) using Notion as primary PM
- Sprint cadence exists (1w / 2w)
- Tasks queried programmatically via Notion API OR planning to ≤30 days

## Skip If (ANY kills it)

- Team >10 people — Notion DB performance degrades
- Strict SOC2/HIPAA compliance with field-level audit requirements
- Native burndown/velocity charts required — use Linear instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Notion workspace + integration token (admin) | config | Notion admin |
| Team roster + assignee identities (Notion or email) | table | people doc |
| Sprint cadence + start-day decision | doc | team agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/capacity-fit-calculator` | Peer methodology — reads Tasks DB rollups for velocity inputs. |
| `solo/pm/pm-agile/linear-issue-tracking` | Peer methodology — comparison baseline; Notion picks here, Linear there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-notion-pm` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-notion-pm` | haiku | Schema check + threshold checks; deterministic. |
| `review-notion-pm` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/notion-pm.json` | JSON skeleton conforming to the output contract schema. |
| `templates/notion-pm.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/notion-pm.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/notion-pm.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sprint-template.md.j2` | Notion sprint page template — goal, metrics, backlog view, daily standups, retro. |
| `templates/sprint-template.md` | Notion sprint page template — goal, metrics, backlog view, daily standups, retro. Generated from `templates/sprint-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/task-template.md.j2` | Notion task page template — description, context, acceptance criteria, sub-tasks, update log. |
| `templates/task-template.md` | Notion task page template — description, context, acceptance criteria, sub-tasks, update log. Generated from `templates/task-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[linear-issue-tracking]]
- [[capacity-fit-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/notion-pm.json`

```json
{
  "artefact_id": "notion-pm-2026-q2",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "workspace_url": "https://notion.so/faion",
  "tasks_db_id": "<tasks_db_id>",
  "projects_db_id": "<projects_db_id>",
  "sprints_db_id": "<sprints_db_id>",
  "property_count": 14,
  "integrations": {
    "status_type": "status",
    "pagination_enabled": true,
    "rate_limit_delay_ms": 350,
    "n8n_workflows": [
      "standup-digest",
      "sprint-closure"
    ]
  },
  "owner": "@ruslan"
}
```
