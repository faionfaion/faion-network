---
slug: backup-filesystem-restic
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement encrypted, deduplicated filesystem backups using Restic (modern, cloud-native S3/B2/REST backends) or BorgBackup (compression-focused, SSH-based).
content_id: "3eec1d7d76f50d39"
tags: [backup, restic, borgbackup, filesystem, encryption]
---
# Filesystem Backup with Restic and BorgBackup

## Summary

**One-sentence:** Implement encrypted, deduplicated filesystem backups using Restic (modern, cloud-native S3/B2/REST backends) or BorgBackup (compression-focused, SSH-based).

**One-paragraph:** Implement encrypted, deduplicated filesystem backups using Restic (modern, cloud-native S3/B2/REST backends) or BorgBackup (compression-focused, SSH-based). Both tools deduplicate at the chunk level to reduce storage costs. Automate with systemd timers and prune retention policies.

## Applies If (ALL must hold)

- Backing up application data directories, /etc, /home, or /var/www to cloud object storage (S3, Backblaze B2, Wasabi).
- Environments where deduplication matters — large media files, log archives, database export directories with repeated content.
- When encryption at the source is required (PII, compliance) — Restic and Borg encrypt before transmission.
- Multi-server environments where a central Borg server or Restic REST server receives backups from many hosts.
- Replacing legacy rsync-only backup setups that lack encryption and deduplication.

## Skip If (ANY kills it)

- Kubernetes PersistentVolume backups — use Velero with CSI snapshots instead; Restic/Borg do not understand K8s resource state.
- Database hot backups — run pg_dump/XtraBackup/mongodump first, then send the export file to Restic for offsite copy.
- Environments where object storage is the primary store (S3 with versioning enabled) — backup the source, not the bucket replica.

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
