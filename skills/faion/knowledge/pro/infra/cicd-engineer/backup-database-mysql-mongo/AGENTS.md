---
slug: backup-database-mysql-mongo
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement MySQL/MariaDB backups with mysqldump (logical, portable) and Percona XtraBackup (hot physical, no locking for InnoDB).
content_id: "97b13b2a19a63534"
tags: [backup, mysql, mongodb, xtrabackup, database]
---
# MySQL and MongoDB Backup Implementation

## Summary

**One-sentence:** Implement MySQL/MariaDB backups with mysqldump (logical, portable) and Percona XtraBackup (hot physical, no locking for InnoDB).

**One-paragraph:** Implement MySQL/MariaDB backups with mysqldump (logical, portable) and Percona XtraBackup (hot physical, no locking for InnoDB). Implement MongoDB backups with mongodump including oplog capture for point-in-time recovery on replica sets.

## Applies If (ALL must hold)

- Setting up MySQL/MariaDB backup pipelines for databases that cannot afford write locking during backup.
- Implementing binary-log-based PITR for MySQL — requires binary logging enabled plus a base backup.
- MongoDB replica set backups requiring consistency across collections (requires --oplog).
- Large MySQL databases (50+ GB) where mysqldump takes too long — switch to XtraBackup hot backup.
- Migrating MySQL databases between environments using mysqldump portable SQL format.

## Skip If (ANY kills it)

- Fully managed services (RDS MySQL, Atlas MongoDB) where the provider already supplies automated backups — unless cross-account copies are needed.
- Stateless microservices that reconstruct their state from event streams — backing up derived state is waste.
- MongoDB Atlas with built-in cloud backup enabled and no cross-cloud requirement.

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
