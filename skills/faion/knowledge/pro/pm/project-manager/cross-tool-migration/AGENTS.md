---
slug: cross-tool-migration
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six-phase ETL process for migrating a project management tool portfolio between Jira, Linear, Asana, ClickUp, GitHub Projects, Azure DevOps, and others.
content_id: "73e35e833df8afe9"
tags: [migration, pm-tools, etl, data-integrity, cutover]
---
# Cross-Tool Migration

## Summary

**One-sentence:** Six-phase ETL process for migrating a project management tool portfolio between Jira, Linear, Asana, ClickUp, GitHub Projects, Azure DevOps, and others.

**One-paragraph:** Six-phase ETL process for migrating a project management tool portfolio between Jira, Linear, Asana, ClickUp, GitHub Projects, Azure DevOps, and others. Migration runs in waves: pilot one project first, validate, then full waves. Source goes read-only at T-4h cutover; source stays live in read-only for 30 days after. Auto-cutover is forbidden — a human declares go-live.

## Applies If (ALL must hold)

- Migrating a portfolio between PM tools after a tooling decision, acquisition, or consolidation.
- Cloud relocation within the same vendor (Jira Server/DC to Cloud) — same risk profile.
- Splitting one tracker into multiple tools (engineering to Linear, marketing to Asana).
- Pairing with pm-tool-selection (decide first), change-control (cutover gate), communications-management (change comms plan), lessons-learned (post-cutover).

## Skip If (ANY kills it)

- Tool unhappiness without root-cause diagnosis — most complaints reduce to bad workflows; fix that first.
- Active feature freeze, audit window, or year-end close — wait for lower-traffic periods.
- Solo or very small teams (under 10 users, under 500 issues) — copy by hand, do not build a pipeline.
- When the source tool has critical custom plugins (Tempo, Insight) with no target equivalents — resolve the gap before migration.

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

- parent skill: `pro/pm/project-manager/`
