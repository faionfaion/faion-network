---
slug: clickup-setup
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ClickUp workspace architecture: 4-level hierarchy (Workspace → Space → Folder → List), ClickApps configuration (Sprints, Time Tracking, Custom Fields, Priorities, Multiple Assignees), custom status workflow per space, views (List, Board, Gantt, Workload, Dashboard), and automation rules for status transitions and template application.
content_id: "2057512c14519cb0"
tags: [clickup, project-management, task-tracking, team-coordination, workflow-automation]
---
# ClickUp Setup

## Summary

**One-sentence:** ClickUp workspace architecture: 4-level hierarchy (Workspace → Space → Folder → List), ClickApps configuration (Sprints, Time Tracking, Custom Fields, Priorities, Multiple Assignees), custom status workflow per space, views (List, Board, Gantt, Workload, Dashboard), and automation rules for status transitions and template application.

**One-paragraph:** ClickUp workspace architecture: 4-level hierarchy (Workspace → Space → Folder → List), ClickApps configuration (Sprints, Time Tracking, Custom Fields, Priorities, Multiple Assignees), custom status workflow per space, views (List, Board, Gantt, Workload, Dashboard), and automation rules for status transitions and template application. Create custom fields at the highest applicable level (Workspace > Space > Folder) to avoid duplication.

## Applies If (ALL must hold)

- Starting a new organization that needs PM, docs, and time tracking in one tool
- Migrating from a simpler tool (Trello, Asana) when the team has outgrown it
- Cross-functional team with different workflows per department (Engineering uses Sprints; Marketing uses a content calendar)
- OKR and goal tracking needed alongside task management
- Time tracking and billing required

## Skip If (ANY kills it)

- Team is already on GitHub and needs code-task traceability — GitHub Projects is a better fit
- Solo developer or very small team — ClickUp's hierarchy adds setup overhead that exceeds its value at this scale
- Team primarily needs kanban with minimal configuration — Trello is simpler and faster to adopt
- Technical team values keyboard-first, minimal-config workflows — Linear is a better fit

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
