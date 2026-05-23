# PostgreSQL Backup Implementation

## Summary

**One-sentence:** Generates a production PostgreSQL backup pipeline (pg_dump / pg_basebackup / pgBackRest + WAL archiving) with integrity verification, S3 offsite copy, and PITR-ready WAL monitoring.

**One-paragraph:** PostgreSQL has two distinct backup surfaces — logical (`pg_dump`, `pg_dumpall`) and physical (`pg_basebackup`, pgBackRest). Logical dumps are portable and row-granular but cannot do PITR. Physical backups preserve the binary cluster state and, combined with WAL archiving, allow restore to any point in time — the only remedy for logical corruption (e.g. UPDATE without WHERE) that replicates to replicas immediately. Over half of "successful" backups fail at restore time because no integrity check ran after creation. This methodology emits a script bundle that always verifies before upload, monitors `pg_stat_archiver.failed_count`, encrypts at rest, and tags every artifact for selective restore.

**Ефективно для:**

- Standing up nightly logical dumps with offsite S3 copy and 30-day retention.
- Enabling PITR via WAL archiving + `pg_basebackup` base backup with failure-count monitoring.
- Migrating multi-GB databases between environments via custom format + parallel restore.
- Implementing compliance-grade retention (daily/weekly/monthly) with periodic restore drills.
- Replacing ad-hoc cron `pg_dump | gzip > file` with a verified, alerted pipeline.

## Applies If (ALL must hold)

- Self-managed PostgreSQL 13+ (RDS / Cloud SQL managed backups not sufficient or cross-cloud copy required).
- Backup target supports either S3-compatible object storage or a Restic / pgBackRest repository.
- Recovery objective (RPO/RTO) is documented and ≥ 1 minute (PITR target).

## Skip If (ANY kills it)

- Fully managed PaaS (RDS / Cloud SQL / AlloyDB) with automated backups enabled and no cross-account copy requirement.
- Stateless data derived entirely from upstream (Git, S3 with versioning) — backing up derived state is waste.
- Dev-only single-VM environment with no recovery requirement — a local cron `pg_dump` is sufficient.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Database connection params | env (`PGHOST`, `PGUSER`, `PGDATABASE`) | Vault / Secrets Manager |
| Backup target | S3 bucket URI or pgBackRest stanza name | Infra catalog |
| Retention policy | days (local) + days (remote) | Compliance / team policy |
| WAL archive command | shell snippet | `postgresql.conf` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[backup-verification-dr]] | Restore drills + monitoring complement the producer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (verify-before-upload, WAL archive monitoring, custom format, secret hygiene, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the pipeline config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (no-verify, silent WAL gap, secret in git) with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure (scope → script → verify → upload → monitor) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement on RPO/RTO + infra. |
| `draft-backup-pipeline` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/postgres-backup.sh` | pg_dump + verify + S3 push script skeleton |
| `templates/pgbackrest.conf` | pgBackRest stanza config with retention + encryption |
| `templates/backup-config.example.json` | Filled config artefact conforming to the schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-database-postgres.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[backup-filesystem-restic]]
- [[backup-verification-dr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (managed-PaaS-or-not, PITR required, RPO target) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
