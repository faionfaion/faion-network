---
slug: backup-filesystem-restic
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an encrypted filesystem backup pipeline using Restic (or BorgBackup) with S3/B2 backend, retention policy, weekly repo check, and systemd timer wiring.
content_id: "431f139632d3bb44"
complexity: medium
produces: config
est_tokens: 4200
tags: ["backup", "restic", "borgbackup", "filesystem", "encryption"]
---
# Filesystem Backup with Restic

## Summary

**One-sentence:** Generates an encrypted filesystem backup pipeline using Restic (or BorgBackup) with S3/B2 backend, retention policy, weekly repo check, and systemd timer wiring.

**One-paragraph:** Filesystem Backup with Restic — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Self-hosted hosts with persistent filesystem state (databases dumps, mailspools, /etc, user homes) requiring offsite copy.
- Encryption-at-rest mandated by compliance or cross-tenant data handling.
- Retention discipline (daily/weekly/monthly) over rolling tarballs.

## Applies If (ALL must hold)

- Self-hosted hosts with persistent filesystem state (databases dumps, mailspools, /etc, user homes) requiring offsite copy.
- Encryption-at-rest mandated by compliance or cross-tenant data handling.
- Retention discipline (daily/weekly/monthly) over rolling tarballs.

## Skip If (ANY kills it)

- Cloud-native VMs with infra-managed snapshots already covering RPO/RTO.
- Ephemeral CI runner filesystems with no durable state.

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
| `content/01-core-rules.xml` | essential | 6 testable rules (password-from-secrets-manager, weekly-repo-check, forget-with-prune, exclude-volatile-paths, systemd-timer-not-cron, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-backup-filesystem-restic` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backup-restic.sh` | Restic backup + forget --prune + weekly check skeleton |
| `templates/backup.timer` | systemd timer skeleton |
| `templates/backup.service` | systemd service skeleton invoking backup-restic.sh |
| `templates/backup-config.example.json` | Filled config artefact conforming to the schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-filesystem-restic.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[backup-database-postgres]]
- [[backup-kubernetes-velero]]
- [[backup-verification-dr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
