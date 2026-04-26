# ClickUp Setup

## Summary

ClickUp workspace architecture: 4-level hierarchy (Workspace → Space → Folder → List), ClickApps configuration (Sprints, Time Tracking, Custom Fields, Priorities, Multiple Assignees), custom status workflow per space, views (List, Board, Gantt, Workload, Dashboard), and automation rules for status transitions and template application. Create custom fields at the highest applicable level (Workspace > Space > Folder) to avoid duplication.

## Why

ClickUp combines task tracking, docs, goals, and time tracking in one tool, making it suited for cross-functional teams that would otherwise need multiple SaaS subscriptions. The workspace hierarchy separates permissions and workflows by team while sharing a single workspace. Automation rules reduce manual status management and enforce consistent task structure via templates.

## When To Use

- Starting a new organization that needs PM, docs, and time tracking in one tool
- Migrating from a simpler tool (Trello, Asana) when the team has outgrown it
- Cross-functional team with different workflows per department (Engineering uses Sprints; Marketing uses a content calendar)
- OKR and goal tracking needed alongside task management
- Time tracking and billing required

## When NOT To Use

- Team is already on GitHub and needs code-task traceability — GitHub Projects is a better fit
- Solo developer or very small team — ClickUp's hierarchy adds setup overhead that exceeds its value at this scale
- Team primarily needs kanban with minimal configuration — Trello is simpler and faster to adopt
- Technical team values keyboard-first, minimal-config workflows — Linear is a better fit

## Content

| File | What's inside |
|------|---------------|
| `content/01-workspace-setup.xml` | Hierarchy rules, ClickApps config, custom status workflow, custom fields rules |
| `content/02-automation-views.xml` | Automation rule patterns, view types and their purposes, integration setup rules |

## Templates

none
