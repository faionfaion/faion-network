# Trello Kanban

## Summary

Trello is a card-based kanban tool where work items move left-to-right through 5–7 named lists. Boards are the fastest PM setup for visual thinkers and non-technical stakeholders. Butler automation handles mechanical card moves without custom code. WIP limits are enforced by embedding them in list names (e.g., "In Progress [WIP:3]").

## Why

Trello's visual model eliminates the overhead of database schemas and custom fields required by heavier tools. For small teams with linear flows, the board IS the process — no configuration layer between the team and their work. Butler rules handle 90% of repetitive moves (auto-archive, auto-assign) as English natural-language rules, keeping automation accessible to non-developers.

## When To Use

- Small teams (2–8 people) needing a visual board fast without field configuration
- Non-technical stakeholders (marketing, ops, content) who find Jira or Linear intimidating
- Projects with a simple linear flow: cards move left-to-right through defined stages
- Butler automation covers most repetitive moves without custom code
- Prototyping a new workflow before committing to a heavier tool

## When NOT To Use

- Engineering teams needing native Git/PR integration — Trello's GitHub Power-Up is shallow
- Projects requiring sub-tasks, epics, or multi-level hierarchy — cards are flat; checklists are a poor substitute
- Teams needing velocity tracking, cycle time analytics, or burndown charts without third-party Power-Ups
- Large backlogs (500+ cards) — board performance degrades and visual scanning becomes impractical
- Organizations requiring SSO, audit logs, or enterprise compliance — Enterprise plan only

## Content

| File | What's inside |
|------|---------------|
| `content/01-board-setup.xml` | Board structure patterns, list naming, WIP limits, card anatomy, label system |
| `content/02-automation.xml` | Butler rules and buttons, Power-Ups configuration, API integration patterns |
| `content/03-agent-usage.xml` | Agentic workflow, recommended subagents, API gotchas, best practices for agent use |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-feature.md` | Feature card description template with user story and acceptance criteria |
| `templates/card-bug.md` | Bug report card template with reproduction steps and severity |
| `templates/butler-rules.yaml` | Butler automation rule examples: sprint flow, stale card alert, blocked escalation |
| `templates/prompt-fetch-cards.txt` | Prompt for agent to fetch and report in-progress cards |
