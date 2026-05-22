---
slug: tool-migration-process
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A phase-by-phase execution playbook for migrating project data between PM tools at org scale: six phases (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilization) with an ETL engine, cutover checklist, rollback strategy, and change-management comms plan.
content_id: "bb584d529cc9a1a8"
tags: [migration, pm-tools, cutover, etl, change-management]
---
# Cross-Tool PM Migration — Process

## Summary

**One-sentence:** A phase-by-phase execution playbook for migrating project data between PM tools at org scale: six phases (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilization) with an ETL engine, cutover checklist, rollback strategy, and change-management comms plan.

**One-paragraph:** A phase-by-phase execution playbook for migrating project data between PM tools at org scale: six phases (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilization) with an ETL engine, cutover checklist, rollback strategy, and change-management comms plan. Designed for migrations touching ≥3 teams, ≥1k issues, or any compliance scope.

## Applies If (ALL must hold)

- You have completed field-mapping and audit (see tool-migration-basics) and need an execution playbook.
- Org-wide migration touching ≥3 teams, ≥1k issues, or a compliance scope.
- Multi-wave migrations where teams cut over in batches across weeks.
- Cutover windows requiring rollback rehearsal and freeze coordination.
- Post-merger consolidation requiring two source tools → one target.

## Skip If (ANY kills it)

- Single-team or <100 issue migration — use basics + a one-day cutover; this playbook adds overhead.
- Vendor-managed migration where their tooling does extract/transform/load — defer to it.
- Migrations during an active product launch or incident — wait for a quieter window.
- Projects where the primary risk is political (team adoption), not technical — invest in change management depth instead.

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
