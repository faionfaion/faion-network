# Cross-Tool PM Migration — Process

## Summary

A phase-by-phase execution playbook for migrating project data between PM tools at org scale: six phases (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilization) with an ETL engine, cutover checklist, rollback strategy, and change-management comms plan. Designed for migrations touching ≥3 teams, ≥1k issues, or any compliance scope.

## Why

Large PM migrations fail most often at two points: data transformation (field mismatches surface only in production) and cutover (rate limits, missing ID mappings, and silent attachment loss). A phase-gated playbook with dry-run-first ETL and rehearsed rollback converts unpredictable cutovers into repeatable operations with clear abort criteria.

## When To Use

- You have completed field-mapping and audit (see `tool-migration-basics`) and need an execution playbook.
- Org-wide migration touching ≥3 teams, ≥1k issues, or a compliance scope.
- Multi-wave migrations where teams cut over in batches across weeks.
- Cutover windows requiring rollback rehearsal and freeze coordination.
- Post-merger consolidation requiring two source tools → one target.

## When NOT To Use

- Single-team or <100 issue migration — use basics + a one-day cutover; this playbook adds overhead.
- Vendor-managed migration where their tooling does extract/transform/load — defer to it.
- Migrations during an active product launch or incident — wait for a quieter window.
- Projects where the primary risk is political (team adoption), not technical — invest in change management depth instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases.xml` | Six migration phases with entry/exit criteria and duration guidance. |
| `content/02-etl-engine.xml` | Python ETL skeleton (extract/transform/load) with dry-run flag, checkpointing, and ID mapping. |
| `content/03-cutover-and-rollback.xml` | Cutover checklist (T-24h through T+1w), rollback triggers, comms plan template. |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-plan.md` | Project plan template: scope, timeline, risk register, success criteria. |
| `templates/load_resume.py` | Checkpointed loader — resumes from `.checkpoint` on rerun; handles rate-limit backoff. |

