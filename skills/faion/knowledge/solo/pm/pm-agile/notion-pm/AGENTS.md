# Notion PM

## Summary

Notion PM uses interconnected databases (Projects, Tasks, Sprints) with relation and rollup fields to build a customizable agile workspace. Tasks must exist as individual database pages — not as sub-bullets inside sprint documents — to be queryable via the API. Use a single Tasks database with Sprint as a relation field; never create a new database per sprint, which fragments history and breaks velocity computation.

## Why

Notion combines task tracking and documentation in one workspace, eliminating the PM-tool + wiki context switch. Its flexible database structure adapts to evolving processes faster than Jira or Linear. Stakeholders get read-only access via a shareable page without creating PM accounts. The Notion API supports full CRUD on pages and databases, enabling agent-driven sprint planning, standup digests, and sprint closure workflows.

## When To Use

- Small agile team (2–10 people) wanting sprint planning, backlog, and docs in one tool
- When sprint retrospectives, meeting notes, and task tracking need inline cross-references
- When workflow is still evolving — Notion databases restructure faster than Jira or Linear
- Solopreneur or micro-team where full sprint tooling (velocity charts, burndowns) is overkill
- When stakeholders need read-only project status via shareable page without PM tool accounts

## When NOT To Use

- Teams with mature Scrum practices needing native burndown charts, velocity tracking, and sprint analytics
- High-velocity engineering teams with 10+ members — database performance degrades with large datasets
- When issues need tight Git/PR integration (auto-close on merge, branch naming)
- Organizations needing SOC2/HIPAA compliant issue tracking with field-level audit logs

## Content

| File | What's inside |
|------|---------------|
| `content/01-database-design.xml` | Projects and Tasks database schemas, relations, rollups, formula examples |
| `content/02-views-automations.xml` | Board/table/timeline/calendar view configs, native automations, Zapier/n8n patterns |
| `content/03-agent-usage.xml` | Agentic sprint cycle, subagent patterns, API rate limits, Python sprint assignment script |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-template.md` | Notion task page template with context, acceptance criteria, and updates log |
| `templates/sprint-template.md` | Sprint page template with goal, metrics, backlog, standups, and retrospective |
| `templates/prompt-sprint-planner.txt` | Prompt for agent to select and assign backlog tasks to a sprint |
