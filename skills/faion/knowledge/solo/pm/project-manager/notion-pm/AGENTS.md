---
slug: notion-pm
tier: solo
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Notion's relational databases let teams connect tasks, projects, docs, and meeting notes in one tool.
content_id: "ae344d00cc415537"
tags: [notion, databases, relational, task-management, rollups]
---
# Notion for Integrated Docs and Task Management

## Summary

**One-sentence:** Notion's relational databases let teams connect tasks, projects, docs, and meeting notes in one tool.

**One-paragraph:** Notion's relational databases let teams connect tasks, projects, docs, and meeting notes in one tool. Relations and rollups replace spreadsheet-based status tracking: task count per project, total story points, completion percentage — all computed automatically. The REST API uses the same database_id and property names as the UI, making it the most straightforward PM tool API for agent integration. Limit database properties to 15-20 per database — complex formulas and too many relations degrade performance.

## Applies If (ALL must hold)

- Team wants to combine documentation and task tracking in one workspace.
- Flexible, evolving process that would outgrow a more opinionated tool quickly.
- Rich documentation alongside tasks is essential (RFCs, specs, meeting notes all interlinked).
- Cross-functional teams with diverse workflow needs in one shared workspace.

## Skip If (ANY kills it)

- Team needs code-task traceability ("Fixes #123") — GitHub Projects is a better fit.
- Engineering team needs keyboard-first, high-velocity issue tracking — Linear is faster.
- Simple kanban with no documentation needs — Trello is faster to set up and maintain.
- Performance-critical at scale: Notion databases with 500+ items and complex formulas load slowly.

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

- parent skill: `solo/pm/project-manager/`
