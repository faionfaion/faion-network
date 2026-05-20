---
slug: tool-migration-basics
tier: pro
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured approach to migrating project management data between tools, covering pre-migration audit, field mapping, ETL execution, and post-cutover validation.
content_id: "15e0e56a461dba74"
tags: [migration, pm-tools, data-etl, jira, linear]
---
# Cross-Tool Migration Basics

## Summary

**One-sentence:** A structured approach to migrating project management data between tools, covering pre-migration audit, field mapping, ETL execution, and post-cutover validation.

**One-paragraph:** A structured approach to migrating project management data between tools, covering pre-migration audit, field mapping, ETL execution, and post-cutover validation. The critical rule: run the migration three times — dev test, full dry-run with rollback, real cutover — and preserve source IDs in a legacy_id custom field on the target so every external link and commit message that hardcoded PROJ-1234 still resolves.

## Applies If (ALL must hold)

- Switching PM tools (Jira to Linear, Trello to ClickUp, Asana to Notion).
- Consolidating two or more tools after acquisition or department merge.
- Outgrowing a starter tool (Trello/Notion) onto an enterprise tool (Jira/Azure DevOps).
- Compliance push forces migration to a tool with stronger security posture.
- Current vendor's pricing model becomes hostile (per-seat hike, mandatory tier upgrade).

## Skip If (ANY kills it)

- One person and fewer than 100 issues — re-create them by hand in an afternoon.
- Vendor offers a guided managed migration that already handles data ETL — use it; this brief adds overhead.
- Tool change is driven by hype rather than measurable pain — wait three months and re-evaluate.
- Active product launch or freeze period — defer until after.
- Source data is too dirty to be worth migrating; archive and start fresh.

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

- parent skill: `pro/pm/pm-agile/`
