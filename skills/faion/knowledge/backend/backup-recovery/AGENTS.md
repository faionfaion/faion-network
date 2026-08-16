# Backup and Recovery for Solo VPS

## Summary

**One-sentence:** 3-2-1 backup strategy for solo VPS: PostgreSQL pg_dump -Fc with verify, Redis RDB snapshot, config capture, restic encrypted offsite to B2/S3 with --keep-daily 7 --keep-weekly 4 --keep-monthly 6 retention.

**One-paragraph:** A solo VPS hosts databases, secrets, and configuration that cannot be reconstructed from Git. The 3-2-1 rule (3 copies, 2 media, 1 offsite) is the minimum viable insurance. Restic provides encryption, deduplication, and retention pruning in a single tool. Without tested backups, an RTO of 'hours' becomes 'days or never'. This methodology produces a versioned backup report with verified dumps + restic snapshot IDs + RPO/RTO numbers anchored to actual restore drills.

## Applies If (ALL must hold)

- VPS hosts at least one stateful service (DB, cache, secrets).
- Operator can run a weekly cron and store credentials in 1Password / Bitwarden.
- Offsite storage (B2 / S3) account is funded.

## Skip If (ANY kills it)

- Ephemeral data fully reconstructable from Git + external APIs.
- All persistence in managed cloud DB with provider-side backups verified.
- Single-day prototype with no real users.

**Ефективно для:**

- Соло-фаундери з Postgres + Redis на одному VPS.
- Indie hackers після першого incident коли база впала.
- Регулярні restore-drills для аудиту (SOC2 / GDPR).
- Дешева страховка: $5/міс B2 → нескінченний sleep при datacenter fire.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/cron-automation` | Daily backup runs from cron. |
| `solo/infra/server-craft/secrets-management` | Restic password lives in vault. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown backup-and-recovery report with verified dumps + restic snapshots. |
| `templates/skeleton.md` | Markdown backup-and-recovery report with verified dumps + restic snapshots. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in backup report. |
| `templates/_smoke-test.md` | Minimum viable filled-in backup report. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/backup.sh` | Daily backup orchestrator: pg_dump + verify + Redis + configs + restic + retention. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-recovery.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[cron-automation]]
- [[monitoring-logging]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backup.sh`

```bash
#!/usr/bin/env bash
# Run daily from cron at 03:00.
set -euo pipefail

BACKUP_ROOT=/home/nero/backups
STAMP=$(date +%Y%m%d)

# 1. Postgres
docker exec -t nero-postgres pg_dump -U nero -Fc nero_db \
  > "$BACKUP_ROOT/database/nero_db_${STAMP}.dump"
pg_restore --list "$BACKUP_ROOT/database/nero_db_${STAMP}.dump" >/dev/null \
  || { echo CORRUPT; exit 1; }

# 2. Redis RDB
docker cp nero-redis:/data/dump.rdb "$BACKUP_ROOT/redis/dump_${STAMP}.rdb"

# 3. Configs
tar -czf "$BACKUP_ROOT/configs/configs_${STAMP}.tgz" /etc/nginx /etc/systemd /etc/wireguard

# 4. Restic offsite + retention
export RESTIC_PASSWORD_FILE=/root/.restic-password
restic backup "$BACKUP_ROOT" --tag daily --quiet
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune --quiet

# 5. Local retention
find "$BACKUP_ROOT" -mtime +14 -delete
```
