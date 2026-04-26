# Cross-Tool Migration

## Summary

Six-phase ETL process for migrating a project management tool portfolio between Jira, Linear, Asana, ClickUp, GitHub Projects, Azure DevOps, and others. Migration runs in waves: pilot one project first, validate, then full waves. Source goes read-only at T-4h cutover; source stays live in read-only for 30 days after. Auto-cutover is forbidden — a human declares go-live.

## Why

Migrating PM tools carries high silent failure risk: field mappings degrade gracefully (issues migrate but lose priority, links, assignees), and the migration logs say "success" while data integrity fails. Two-pass loading (create issues, then re-create links using id-map) and wave-based execution with human gates between waves are the primary mechanisms that prevent silent data loss from reaching production.

## When To Use

- Migrating a portfolio between PM tools after a tooling decision, acquisition, or consolidation.
- Cloud relocation within the same vendor (Jira Server/DC to Cloud) — same risk profile.
- Splitting one tracker into multiple tools (engineering to Linear, marketing to Asana).
- Pairing with pm-tool-selection (decide first), change-control (cutover gate), communications-management (change comms plan), lessons-learned (post-cutover).

## When NOT To Use

- Tool unhappiness without root-cause diagnosis — most complaints reduce to bad workflows; fix that first.
- Active feature freeze, audit window, or year-end close — wait for lower-traffic periods.
- Solo or very small teams (under 10 users, under 500 issues) — copy by hand, do not build a pipeline.
- When the source tool has critical custom plugins (Tempo, Insight) with no target equivalents — resolve the gap before migration.

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases-and-rules.xml` | Six-phase process, two-pass load rule, identity remapping, read-only window, rollback triggers. |
| `content/02-field-mapping.xml` | Field mapping design, low-confidence flagging, attachment ordering, anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-project-plan.md` | Full migration plan with scope, timeline, risk register, success criteria. |
| `templates/cutover-checklist.md` | T-24h / T-4h / T-0 / T+1h / T+24h / T+1w cutover runbook. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/migrate_dry_run.sh` | Extract, transform, count-diff, field-drift audit — gate before each wave. |
