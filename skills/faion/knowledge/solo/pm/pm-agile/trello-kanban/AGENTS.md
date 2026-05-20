---
slug: trello-kanban
tier: solo
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Trello is a card-based kanban tool where work items move left-to-right through 5–7 named lists.
content_id: "3062f115860d560f"
tags: [trello, kanban, pm, board, automation]
---
# Trello Kanban

## Summary

**One-sentence:** Trello is a card-based kanban tool where work items move left-to-right through 5–7 named lists.

**One-paragraph:** Trello is a card-based kanban tool where work items move left-to-right through 5–7 named lists. Boards are the fastest PM setup for visual thinkers and non-technical stakeholders. Butler automation handles mechanical card moves without custom code. WIP limits are enforced by embedding them in list names (e.g., "In Progress [WIP:3]").

## Applies If (ALL must hold)

- Small teams (2–8 people) needing a visual board fast without field configuration
- Non-technical stakeholders (marketing, ops, content) who find Jira or Linear intimidating
- Projects with a simple linear flow: cards move left-to-right through defined stages
- Butler automation covers most repetitive moves without custom code
- Prototyping a new workflow before committing to a heavier tool

## Skip If (ANY kills it)

- Engineering teams needing native Git/PR integration — Trello's GitHub Power-Up is shallow
- Projects requiring sub-tasks, epics, or multi-level hierarchy — cards are flat; checklists are a poor substitute
- Teams needing velocity tracking, cycle time analytics, or burndown charts without third-party Power-Ups
- Large backlogs (500+ cards) — board performance degrades and visual scanning becomes impractical
- Organizations requiring SSO, audit logs, or enterprise compliance — Enterprise plan only

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/pm/pm-agile/`
