---
slug: backup-kubernetes-velero
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Velero installation + Schedule CRDs + CSI snapshot wiring + Kopia data mover config for full + namespace-scoped cluster backups with pre/post hooks for stateful apps.
content_id: "3bebced61f73fc4d"
complexity: medium
produces: config
est_tokens: 4300
tags: ["backup", "velero", "kubernetes", "csi-snapshots", "kopia"]
---
# Kubernetes Cluster Backup with Velero

## Summary

**One-sentence:** Generates a Velero installation + Schedule CRDs + CSI snapshot wiring + Kopia data mover config for full + namespace-scoped cluster backups with pre/post hooks for stateful apps.

**One-paragraph:** Kubernetes Cluster Backup with Velero — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Self-managed Kubernetes 1.27+ with CSI snapshots enabled.
- Stateful workloads (Postgres, Mongo, file-volumes) requiring consistent multi-resource backup.
- DR strategy needs namespace-scoped restore and cluster migration capability.

## Applies If (ALL must hold)

- Self-managed Kubernetes 1.27+ with CSI snapshots enabled.
- Stateful workloads (Postgres, Mongo, file-volumes) requiring consistent multi-resource backup.
- DR strategy needs namespace-scoped restore and cluster migration capability.

## Skip If (ANY kills it)

- GitOps-only cluster: every workload is reconciled from Git + external object storage; no in-cluster state needs backup.
- Hosted control plane (EKS/GKE/AKS) where in-cluster state is fully derived from upstream sources.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[backup-database-postgres]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (velero-1-15-no-restic, csi-snapshots-enabled, pre-post-hooks-for-stateful, backup-storage-location-separate-cloud, schedule-retention, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-backup-kubernetes-velero` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/velero-schedule.yaml` | Velero Schedule CRD with hooks + ttl |
| `templates/backup-storage-location.yaml` | Cross-region BackupStorageLocation skeleton |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-kubernetes-velero.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[backup-database-postgres]]
- [[backup-filesystem-restic]]
- [[backup-verification-dr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
