# Notion for Integrated Docs and Task Management

## Summary

**One-sentence:** Notion PM stack with 3 relational DBs (Projects/Tasks/Sprints), Status property + Rollups, purpose-specific views, and a rate-limited REST API integration for agent task management.

**One-paragraph:** Notion's relational databases connect tasks, projects, docs, and meeting notes in one tool. The canonical schema is three databases (Projects, Tasks, Sprints) linked bidirectionally with rollups computing completion, velocity, and points without manual aggregation. Property count is capped at 15-20 per database; archive done items >90 days; cache property names exactly as the API is case-sensitive; rate-limit calls at <=3 req/sec; pagination is mandatory at 100/req. The output is a workspace spec + REST integration record reviewable in code.

**Ефективно для:**

- Solo or 1-5 person team combining tasks + docs in one workspace.
- Cross-functional teams with mixed workflow needs (RFCs alongside Kanban).
- Agent-driven task creation/update via Notion API.
- Replacing spreadsheet status tracking with Rollup-driven progress %.

## Applies If (ALL must hold)

- Team wants to combine documentation and task tracking in one workspace.
- Flexible, evolving process that would outgrow a more opinionated tool.
- Rich documentation alongside tasks is essential (RFCs, specs, meeting notes interlinked).
- Cross-functional teams with diverse workflow needs in one shared workspace.

## Skip If (ANY kills it)

- Team needs code-task traceability ("Fixes #123") — GitHub Projects is a better fit.
- Engineering team needs keyboard-first, high-velocity issue tracking — Linear is faster.
- Simple kanban with no documentation needs — Trello is faster to set up and maintain.
- Performance-critical at scale: Notion databases with 500+ items + complex formulas load slowly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Notion workspace + integration token | env var `NOTION_TOKEN` | platform |
| Database IDs (Projects, Tasks, Sprints) | env vars / config | operator |
| Property schema decisions (Status options, Estimate units, Sprint relation) | ADR | tech-lead |
| Rate-limit budget + retry policy | config | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[reporting-dashboards]] | Downstream consumer of notion query results for status reports. |
| [[trello-kanban]] | Alternative kanban tool — decision-tree compares the two. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 3-database schema, ≤20 props/db, Status not Select, Rollups not formulas, archive >90d, rate-limit 3 req/s | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for notion-pm config artefact + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: formula-iteration, deleted-page rollup orphan, silent rate-limit, property-name mismatch | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold 3 DBs → set relations + rollups → views → API integration → archive policy | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping inputs → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema_design` | sonnet | DB layout + relation map needs judgement. |
| `rollup_authoring` | sonnet | Formula vs rollup decision per metric. |
| `api_integration` | sonnet | Property-name resolution + rate-limit handling. |
| `archive_policy` | haiku | Cron-style cutoff rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-template.md` | Sprint page template with goal, metrics, backlog, retro |
| `templates/task-template.md` | Task page template with description, AC, sub-tasks, updates |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-notion-pm.py` | Validate notion-pm config artefact against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[trello-kanban]]
- [[reporting-dashboards]]
- [[status-report-templates-by-audience]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by team size, doc-vs-issue need, code-traceability requirement, and DB scale onto a rule from `content/01-core-rules.xml`. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
