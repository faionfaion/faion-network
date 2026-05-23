# Status Report Templates by Audience

## Summary

**One-sentence:** Four mandatory status report templates segmented by audience (CEO, PMO, Technical Sponsor, Internal Leadership), each with a different shape, opening hook, and escalation threshold — replacing the generic weekly client status email.

**One-paragraph:** A weekly client status report that goes to the CEO, PMO chief, technical sponsor, AND internal VP at the same length and tone is read by none of them. The CEO needs three numbers and a risk; the PMO needs RAG status against the plan; the technical sponsor needs scope and blockers; the internal VP needs "is this PM in control". This methodology gives the solo PM four ready-to-fork templates, an audience-map rule for picking the right one per stakeholder, and a single source spreadsheet that the four reports are generated from.

**Ефективно для:**

- Solo PM with ≥3 stakeholder roles across one or more clients.
- Client engagements ≥4 weeks long (single-week jobs don't need this).
- Replacing a generic weekly email that has stopped being read.
- Calibrating which audience needs RAG vs prose vs technical detail.

## Applies If (ALL must hold)

- The PM owns weekly status communication for at least one external client OR internal leadership stakeholder.
- Multiple stakeholder roles exist (not a single contact who plays all roles).
- The project runs ≥4 weeks (one-week engagements do not need this).
- Stakeholders' time is scarce (>2h/week of meetings already; cannot absorb 1500-word reports).

## Skip If (ANY kills it)

- Single stakeholder = single template; do not over-engineer.
- The client has imposed a status report format — use theirs.
- Project is in active distress / rescue mode → use a daily standup brief, not weekly reports.
- Reporting fatigue is so high stakeholders explicitly asked for less — drop reports, switch to async demo videos.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source spreadsheet / Notion DB (milestone, RAG, owner, due date, blocker, budget) | sheet | PM |
| Audience map: name + role + template assignment | YAML / sheet | PM |
| Delivery channel per audience (email / Slack / portal) | config | PM |
| One drafted CEO-tier report used as calibration sample | markdown | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[reporting-dashboards]] | The source spreadsheet often comes from the reporting pipeline. |
| [[solo-launch-day-runbook]] | Launch-week status reports follow this audience split. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: audience-mapped template, single source spreadsheet, CEO 5-line cap, RAG before prose, separate technical from leadership | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for the 4-template emission record + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: one-size-fits-all, audience-prose-bleed, source-drift, raw technical in leadership | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure: source → audience map → generate 4 → review → deliver | ~800 |
| `content/05-examples.xml` | essential | Worked example: 4 reports generated from one sheet for a week-7-of-12 project | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audience_map_validation` | haiku | Closed list check. |
| `ceo_5_line_emit` | sonnet | Compression discipline; per-week judgement. |
| `pmo_rag_emit` | haiku | Mechanical table generation from RAG column. |
| `sponsor_blockers_emit` | sonnet | Pick the right 3 blockers + decisions. |
| `leadership_translation` | opus | Translate raw technical into business impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ceo-template.md` | 5-line CEO email body |
| `templates/pmo-template.md` | RAG-first PMO report |
| `templates/sponsor-template.md` | Technical sponsor scope+blockers report |
| `templates/leadership-template.md` | Internal leadership narrative report |
| `templates/audience-map.yaml` | Stakeholder → template map |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-status-report-templates-by-audience.py` | Validate the emission record against 02-output-contract | Friday before send |

## Related

- [[reporting-dashboards]]
- [[notion-pm]]
- [[solo-launch-day-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by stakeholder role, source-spreadsheet presence, CEO-line-count, RAG-position, and technical-language-leak onto a rule from `content/01-core-rules.xml`. Walk it before every Friday distribution.
