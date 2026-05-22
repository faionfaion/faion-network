---
slug: backup-recovery
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Backup strategy and disaster recovery for solo developer VPS platforms: PostgreSQL with pg_dump, Redis RDB snapshots, configuration file capture, and encrypted offsite backup via restic to Backblaze B2 or S3-compatible storage.
content_id: "4bacdd611853b443"
tags: [backup, disaster-recovery, postgresql, restic, 3-2-1]
---
# Backup and Recovery Strategy for Solo VPS

## Summary

**One-sentence:** Backup strategy and disaster recovery for solo developer VPS platforms: PostgreSQL with pg_dump, Redis RDB snapshots, configuration file capture, and encrypted offsite backup via restic to Backblaze B2 or S3-compatible storage.

**One-paragraph:** Backup strategy and disaster recovery for solo developer VPS platforms: PostgreSQL with pg_dump, Redis RDB snapshots, configuration file capture, and encrypted offsite backup via restic to Backblaze B2 or S3-compatible storage. Includes retention policy, restore procedures, and a full disaster recovery runbook.

## Applies If (ALL must hold)

- After initial server bootstrap — set up backups before any data lands
- Before destructive operations: database migrations, major upgrades, config refactors
- As part of an automated nightly cron pipeline
- Creating a disaster recovery runbook for a new project
- Auditing existing backup coverage before a production launch

## Skip If (ANY kills it)

- Ephemeral data that can be fully reconstructed from Git or external APIs
- Application code (already in Git — no separate backup needed)
- Docker images (in registry), Python venvs, node_modules (fully rebuildable)
- Large media files where cloud object storage with versioning is the source of truth

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

- parent skill: `solo/infra/server-craft/`
