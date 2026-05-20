---
slug: backup-kubernetes-velero
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement Kubernetes cluster backup using Velero with CSI volume snapshots and Kopia as the file system backup (FSB) data mover.
content_id: "932dd8abe4a29c8f"
tags: [backup, velero, kubernetes, csi-snapshots, kopia]
---
# Kubernetes Backup with Velero and CSI Snapshots

## Summary

**One-sentence:** Implement Kubernetes cluster backup using Velero with CSI volume snapshots and Kopia as the file system backup (FSB) data mover.

**One-paragraph:** Implement Kubernetes cluster backup using Velero with CSI volume snapshots and Kopia as the file system backup (FSB) data mover. Starting Velero v1.15, Restic is deprecated as the FSB data mover — use Kopia. CSI snapshots are the preferred method for PersistentVolume backups when the storage driver supports them.

## Applies If (ALL must hold)

- Kubernetes clusters running stateful workloads (databases, file stores) that need namespace-level or cluster-level restore capability.
- Multi-namespace applications where a single Velero Schedule covers all namespaces in one backup.
- Disaster recovery drills that require restoring a namespace to a different cluster or region.
- Migrating workloads between clusters or cloud providers using Velero backup + restore to the target.
- Compliance requirements mandating point-in-time recovery for Kubernetes state.

## Skip If (ANY kills it)

- Stateless workloads with no PersistentVolumeClaims — restoring from Git + CI/CD pipeline is faster and more reliable than a Velero restore.
- Databases managed by operators (PostgreSQL, MySQL) — use the operator's native backup mechanism (pgBackRest, XtraBackup) and back up the exports with Restic or Velero as a second layer.
- Clusters on storage drivers that do not support CSI snapshots and where FSB (Kopia) copy time exceeds the backup window.

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
