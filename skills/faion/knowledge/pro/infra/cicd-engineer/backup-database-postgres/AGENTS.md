---
slug: backup-database-postgres
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement PostgreSQL backups using pg_dump for logical snapshots, pg_basebackup for PITR base backups, and pgBackRest for enterprise-grade parallel backup with WAL archiving.
content_id: "d1d93ba83d39b976"
tags: [backup, postgresql, pitr, pgbackrest, database]
---
# PostgreSQL Backup Implementation

## Summary

**One-sentence:** Implement PostgreSQL backups using pg_dump for logical snapshots, pg_basebackup for PITR base backups, and pgBackRest for enterprise-grade parallel backup with WAL archiving.

**One-paragraph:** Implement PostgreSQL backups using pg_dump for logical snapshots, pg_basebackup for PITR base backups, and pgBackRest for enterprise-grade parallel backup with WAL archiving. Verify every backup with an integrity check before uploading to remote storage.

## Applies If (ALL must hold)

- Setting up database backup pipelines for PostgreSQL with offsite copy to S3 or similar object storage.
- Implementing Point-in-Time Recovery (PITR) — requires WAL archiving + base backup.
- Migrating or copying databases between environments using pg_dump custom format.
- Compliance requirements mandate regular backup verification and retention documentation.
- Large databases where parallel dump (-j workers) or incremental backup (pgBackRest) is needed.

## Skip If (ANY kills it)

- Fully managed PaaS (RDS, Cloud SQL, AlloyDB) with automated backups already enabled — unless cross-account or cross-cloud copies are needed.
- Stateless data derived entirely from upstream sources (Git, S3 with versioning) — backing up derived state is waste.
- Dev-only single-VM environments with no recovery requirements — a simple cron pg_dump to local disk is sufficient.

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

- parent skill: `pro/infra/cicd-engineer/`
