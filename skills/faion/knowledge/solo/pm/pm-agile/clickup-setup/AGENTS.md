# ClickUp Setup

## Summary

ClickUp is an all-in-one workspace with a five-level hierarchy (Workspace → Space → Folder → List → Task) and configurable ClickApps per tier. The methodology covers workspace architecture design, custom status and field setup, view configuration, native automations, and API-driven bootstrapping. Create custom fields at the highest applicable level (Space over Folder over List) so they inherit downward — retrofitting field placement after tasks exist requires manual migration.

## Why

ClickUp consolidates project tracking, docs, goals, and time tracking in one tool, eliminating the Trello+Notion+time-tracker stack for cross-functional teams. The hierarchy gives teams isolation (separate Space permissions and workflows per department) while allowing portfolio visibility across Spaces. Native automations handle mechanical status transitions before agents are needed, keeping API call budgets available for high-value operations.

## When To Use

- Starting a new cross-functional workspace where engineering, product, marketing, and ops track work together
- Migrating from Trello or Asana and needing richer hierarchy without switching to Jira
- When OKR/goal tracking alongside task management is required in a single tool
- When time tracking and billing against tasks is needed — ClickUp has built-in estimates
- When highly customizable views (Gantt, Workload, Calendar, Board) are needed without a BI subscription

## When NOT To Use

- Engineering teams needing native Git PR integration as first-class feature — ClickUp's GitHub integration is shallow
- Large enterprises (500+ users) — performance degrades and admin overhead is high
- Simple kanban-only workflows — Trello is faster to set up and maintain
- When the team is already productive in Linear or Jira — migration cost rarely outweighs gains

## Content

| File | What's inside |
|------|---------------|
| `content/01-workspace-setup.xml` | Hierarchy design, ClickApps config, custom status workflow, views, custom fields |
| `content/02-automations.xml` | Native automation examples, integration setup (GitHub, Slack, Toggl) |
| `content/03-agent-usage.xml` | Agentic bootstrapping workflow, recommended subagents, API gotchas, Python script |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-config.json` | Custom status definitions JSON for development workflow |
| `templates/task-template.md` | Task description template with acceptance criteria and checklist |
| `templates/folder-structure.yaml` | Software project folder/list hierarchy example |
| `templates/prompt-bootstrap.txt` | Prompt for agent to create workspace hierarchy via API |
