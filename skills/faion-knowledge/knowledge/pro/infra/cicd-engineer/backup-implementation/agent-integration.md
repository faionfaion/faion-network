# Agent Integration — Backup Implementation

## When to use
- Building backup pipelines for PostgreSQL / MySQL / MongoDB with PITR + offsite copy.
- Implementing 3-2-1 (or 3-2-1-1-0) for filesystems via Restic / Borg / Kopia.
- Kubernetes cluster backup + restore drill (Velero with CSI snapshots, Kopia mover).
- Cloud-native managed backup (AWS Backup, Azure Recovery Services, GCP Backup & DR).
- Automating verification: scheduled restore-to-temp-target with integrity check.
- Hardening against ransomware: object-lock, immutable retention, cross-account copies.

## When NOT to use
- Single-VM dev environment with no recovery requirements — `rsync` + a cron is enough.
- Heavily managed PaaS where backup is already first-class (RDS automated backups, Cloud SQL, Atlas) and you don't need cross-cloud or cross-account copies.
- Stateless workloads where source-of-truth is upstream (Git, S3 with versioning enabled, an event bus). Backing up derived state is waste.
- Compliance-driven contexts where in-house backup violates data-handling rules — use vendor-attested service.

## Where it fails / limitations
- Restic deprecation in Velero v1.15+: agents trained on older docs still emit `--default-volumes-to-restic`. Use Kopia / CSI.
- Snapshot != backup: same-storage-system snapshots fail when the storage system fails. Always copy to a different medium / account / region.
- Encryption key loss = data loss. KMS / passphrase rotation in Restic / Borg can brick a repo if not done atomically.
- Unverified backups: > 50% of "successful" backups fail at restore time. Without a restore drill, you have a recovery theater.
- Logical corruption (an `UPDATE without WHERE`) replicates instantly; you need versioned backups with retention windows, not just replication.
- WAL archive gaps in PITR setups happen silently when the archive command transient-fails — no alert without explicit monitoring.
- Cross-account / cross-region copies + bucket policies are the most common misconfiguration; agents must verify the IAM trust path, not just config success.

## Agentic workflow
Two safe agent surfaces: (1) authoring backup configurations (Restic profiles, Velero schedules, AWS Backup plans, RDS event subscriptions) and committing them as IaC; (2) running restore drills in an isolated account/namespace and reporting integrity. The dangerous surface — running prod restores — must always go through human approval. For day-to-day, an agent reads backup-job status JSON, classifies failures, files tickets, and proposes fixes as PRs. Never let an agent prune / forget / delete a repo.

### Recommended subagents
- A `backup-author` subagent (define inline) — emits Velero `Schedule` YAML, Restic systemd timers, AWS Backup plans, scoped to a target inventory. Read-only on cloud APIs.
- `faion-sdd-executor` — promotes backup IaC through quality gates (lint → dry-run → apply in non-prod → review).
- A `restore-drill` subagent (cron-driven) — picks a random recent backup, restores to scratch namespace/account, runs `pg_dump --schema-only` diff or row-count probes, reports.

### Prompt pattern
```
Generate a Velero Schedule for namespace=<ns>, frequency=daily 02:00 UTC,
TTL=720h, storage location=aws-us-east-1, snapshot location=aws-csi.
Use Kopia data mover (no Restic). Include excluded resources: events, pods.
Output YAML only. After generation, run `velero schedule create --dry-run -f -`
and report any validation error verbatim.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `restic` | Encrypted dedup backup, S3/B2/REST/SFTP backends | https://restic.readthedocs.io/ |
| `borg` / `borgmatic` | Dedup backup with config-driven scheduler | https://borgbackup.readthedocs.io/ , https://torsion.org/borgmatic/ |
| `kopia` | Modern dedup, used as Velero mover | https://kopia.io/ |
| `velero` | K8s cluster + PV backup/restore | https://velero.io/docs/ |
| `pgbackrest` | Postgres PITR with parallel backup | https://pgbackrest.org/ |
| `barman` | Postgres backup manager (alt to pgbackrest) | https://pgbarman.org/ |
| `xtrabackup` | MySQL hot physical backup | https://docs.percona.com/percona-xtrabackup/ |
| `mongodump` / `mongorestore` | MongoDB logical | https://www.mongodb.com/docs/database-tools/mongodump/ |
| `aws backup` (CLI) | Plan, vault, recovery-point CRUD | https://docs.aws.amazon.com/cli/latest/reference/backup/ |
| `s3cmd` / `rclone` | Bucket-to-bucket replication / verification | https://rclone.org/ |
| `restic-runner` / `autorestic` | Cron-friendly wrappers | https://github.com/cupcakearmy/autorestic |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| AWS Backup | SaaS | Yes — REST/CLI | Cross-account, vault-lock for immutability |
| Azure Recovery Services | SaaS | Yes — REST/CLI | Recovery Services Vault, soft delete |
| GCP Backup & DR | SaaS | Yes — gcloud | Successor to Actifio |
| Veeam | SaaS / on-prem | Yes — REST | Mature; heavy Windows + VMware focus |
| Kasten K10 | OSS (paid) / k8s | Yes — kubectl + REST | Velero-class for enterprise k8s |
| Stash by AppsCode | OSS | Partial | Restic-based operator, less active than Velero |
| Backblaze B2 | SaaS | Yes — S3-compatible | Cheap offsite for Restic / rclone |
| Wasabi | SaaS | Yes — S3-compatible | Cheap object lock / immutable bucket |
| pgBackRest Stanza Server | OSS | Yes — file-based | Standard for Postgres PITR |
| Kopia Repository Server | OSS | Yes — REST | Multi-tenant Kopia |

## Templates & scripts
See `templates.md` and `examples.md` for full configs (Velero Schedule, Restic systemd unit, pgBackRest stanza). Inline minimum: nightly Postgres logical backup with verify and S3 push.

```bash
#!/usr/bin/env bash
set -euo pipefail
TS=$(date -u +%Y%m%dT%H%M%SZ)
DUMP=/var/backups/pg/${PGDATABASE}-${TS}.sql.gz
mkdir -p "$(dirname "$DUMP")"
PGPASSWORD="$PGPASSWORD" pg_dump -h "$PGHOST" -U "$PGUSER" "$PGDATABASE" \
  | gzip -9 > "$DUMP"
gunzip -t "$DUMP"                 # integrity check
restic -r "$RESTIC_REPO" backup "$DUMP" --tag "pg,$PGDATABASE,$TS"
restic -r "$RESTIC_REPO" forget --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune
restic -r "$RESTIC_REPO" check --read-data-subset=5%
rm -f "$DUMP"
```

## Best practices
- Verify in the script that emits the backup, not in a separate job — `pg_dump | gzip | gunzip -t` on the same pipe catches corruption in the producer.
- Schedule a restore-drill at least weekly. A backup that has never been restored is undefined behavior.
- Encrypt at the source (Restic / Borg / Kopia). Do not trust the storage layer alone.
- Keep at least one copy in immutable storage (S3 Object Lock + governance retention, or Azure immutable blob).
- Tag every backup with `app`, `env`, `db_role`, `created_by` for selective restore. Velero / AWS Backup honour these.
- Separate retention policies by tier: critical (1y), standard (90d), dev (14d). Single retention on shared repo wastes storage.
- Monitor backup *latency* and *size delta*, not just success. Sudden 10x size = something dumped a wrong path; sudden 0 size = the source is empty.
- For PITR, monitor `pg_stat_archiver` / `pgbackrest info` lag explicitly.
- Air-gap the credentials of the long-term archive account; the daily-runner account can write but not delete.

## AI-agent gotchas
- Restic / Velero have CLI-syntax shifts between minor versions; agents emit deprecated flags (`--default-volumes-to-restic` on Velero ≥ v1.15). Anchor prompt to the exact installed version.
- "Snapshot" is overloaded: EBS snapshot, RDS snapshot, Velero VolumeSnapshot, ZFS snapshot — agents conflate them and write configs that target the wrong layer.
- Generated schedules often forget timezones; "0 2 * * *" without `CRON_TZ=` runs at 2 AM UTC and stomps on traffic peaks for non-UTC teams.
- Object-lock + lifecycle policies interact: a misconfigured lifecycle deletes the index, leaving locked but unreadable data. Always test on a non-prod bucket.
- Encryption key handling: never let an agent commit the Restic password into the repo. Force pull from secrets manager + check via `git diff --staged | grep -E 'RESTIC_PASSWORD|password'` before commit.
- Kopia + S3 requires `KOPIA_PASSWORD` AND `AWS_*`; agents often supply only one and create a half-initialized repo that needs manual recovery.
- Cross-account restore IAM trust paths are tedious; agents output happy-path policies missing `kms:Decrypt` on the source key. Always validate restore in the *target* account, not just write success in source.
- Forget/prune is irreversible. Add a guardrail: agent may emit `forget --dry-run` only; a human runs the real prune.
- Restore-drill agents must isolate scratch resources (separate namespace, separate AWS account if possible) — otherwise a faulty drill can overwrite live data.

## References
- 3-2-1-1-0 Strategy explainer — https://www.veeam.com/blog/321-backup-rule.html
- Velero docs — https://velero.io/docs/main/
- Restic — https://restic.readthedocs.io/en/stable/
- Kopia — https://kopia.io/docs/
- pgBackRest — https://pgbackrest.org/user-guide.html
- AWS Backup — https://docs.aws.amazon.com/aws-backup/latest/devguide/
- Postgres backup chapter — https://www.postgresql.org/docs/current/backup.html
- Cloud Custodian (immutable / orphan tagging) — https://cloudcustodian.io/docs/
