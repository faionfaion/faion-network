---
slug: status-report-templates-by-audience
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "95511be5e005e65a"
summary: Audience-segmented status report templates — CEO, PMO, technical sponsor, internal leadership — that replace the one-size-fits-all weekly status email with reports each audience will actually read.
tags: [status-report, communication, project-manager, solo, pm]
---
# Status Report Templates by Audience

## Summary

**One-sentence:** Four mandatory status report templates segmented by audience (CEO, PMO, technical sponsor, internal leadership), each with a different shape, a different opening hook, and a different escalation threshold — replacing the generic weekly client status email.

**One-paragraph:** A weekly client status report that goes to the CEO, PMO chief, sponsor, AND internal VP at the same length and tone is read by none of them. The CEO needs three numbers and a risk; the PMO needs RAG status against the plan; the technical sponsor needs scope and blockers; the internal VP needs "is this PM in control". This methodology gives a solopreneur PM (or small-team PM) four ready-to-fork templates, an "audience map" rule for picking the right one per stakeholder, and a single source spreadsheet that the four reports are generated from. Output: stakeholders open and read the report instead of asking the PM "so what's happening?" in the next 1:1.

## Applies If (ALL must hold)

- The PM owns weekly status communication for at least one external client OR internal leadership stakeholder.
- Multiple stakeholder roles exist (not a single contact who plays all roles).
- The project runs ≥4 weeks (one-week engagements do not need this).
- Stakeholders' time is scarce (>2h/week of meetings already; cannot absorb 1500-word reports).

## Skip If (ANY kills it)

- Single stakeholder = single template; do not over-engineer.
- The client has imposed a status report format — use theirs and adapt the source spreadsheet to it.
- Project is in active distress / rescue mode → use a daily standup brief, not weekly reports (see `pro/pm/distressed-project-rescue` if present, otherwise improvise).
- Reporting fatigue is already so high stakeholders explicitly asked for less — drop the report entirely and switch to async demo videos.

## Prerequisites

- A single source-of-truth spreadsheet or Notion DB with: milestone, RAG, owner, due date, blocker note, hours spent / budget.
- An audience map: name + role + report template assigned.
- An agreed delivery channel per audience (email vs Slack vs portal upload).
- A draft of one CEO-tier report you would actually send (used to calibrate the others).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/client-status-report-multistyle` | Pro-tier deep-dive; this solo methodology is the entry point. |
| `pro/pm/project-manager/escalation-decision-template` | When the report would say RED → escalation script kicks in. |
| `solo/pm/project-manager/client-visibility-vs-velocity-tradeoff` | Sets the cadence ceiling. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: audience-mapped templates, one-source spreadsheet, CEO 5-line cap, RAG before prose, separate technical from leadership | ~1200 |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodologies: `client-status-email-template-agency` (pro/pm), `client-status-report-multistyle` (pro/pm), `escalation-decision-template` (pro/pm)
- external: [Mike Cohn — Status Reporting Patterns](https://www.mountaingoatsoftware.com/) · [PMI — Stakeholder Communication](https://www.pmi.org/)
