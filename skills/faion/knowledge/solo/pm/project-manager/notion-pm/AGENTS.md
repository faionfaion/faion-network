# Notion PM

## Summary

Notion PM setup: bidirectional relational database design (Projects ↔ Tasks ↔ Sprints), view configuration (Board, Table, Timeline, Calendar), rollup formulas for progress tracking, template system for tasks and sprints, and Notion REST API for agent-driven task management. Limit database properties to 15-20 per database — complex formulas and too many relations degrade performance.

## Why

Notion's relational databases let teams connect tasks, projects, docs, and meeting notes in one tool. Relations and rollups replace spreadsheet-based status tracking: task count per project, total story points, completion percentage — all computed automatically. The REST API uses the same database_id and property names as the UI, making it the most straightforward PM tool API for agent integration.

## When To Use

- Team wants to combine documentation and task tracking in one workspace
- Flexible, evolving process that would outgrow a more opinionated tool quickly
- Rich documentation alongside tasks is essential (RFCs, specs, meeting notes all interlinked)
- Cross-functional teams with diverse workflow needs in one shared workspace

## When NOT To Use

- Team needs code-task traceability ("Fixes #123") — GitHub Projects is a better fit
- Engineering team needs keyboard-first, high-velocity issue tracking — Linear is faster
- Simple kanban with no documentation needs — Trello is faster to set up and maintain
- Performance-critical at scale: Notion databases with 500+ items and complex formulas load slowly

## Content

| File | What's inside |
|------|---------------|
| `content/01-database-design.xml` | Relational database design rules, property type selection, rollup patterns, performance rules |
| `content/02-views-api.xml` | View configuration rules, Notion API patterns, automation with Zapier/Make, formula examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-template.md` | Task page template with description, context, AC, technical notes, sub-tasks |
| `templates/sprint-template.md` | Sprint page template with goal, metrics table, backlog relation, retrospective |
