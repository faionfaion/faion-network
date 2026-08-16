# Backup Strategies (3-2-1-1-0)

## Summary

**One-sentence:** Produces a backup spec applying the 3-2-1-1-0 rule (3 copies, 2 media, 1 offsite, 1 immutable, 0 verified errors) with automated restore verification and RPO/RTO targets.

**One-paragraph:** Modern backup strategy uses the 3-2-1-1-0 rule: 3 copies, 2 media types, 1 offsite, 1 immutable, 0 verified recovery errors. Traditional 3-2-1 fails against ransomware (all 3 copies on network-reachable storage); the 'immutable' copy (S3 Object Lock COMPLIANCE mode, Azure Immutable Blob, WORM tape) survives admin-credential compromise. The '0 errors' clause mandates automated restore verification — backups never tested are not backups. Output is a backup spec naming media, vendors, schedule, retention, immutability mode, RTO/RPO, and the restore-verification job + cadence.

**Ефективно для:**

- Production database / file-system / K8s cluster з DR-вимогою.
- Compliance (GDPR / HIPAA / SOC2 / PCI-DSS) data-retention mandate.
- RPO < 24h business requirement.
- Ransomware protection — частина security posture.

## Applies If (ALL must hold)

- Workload has persistent state worth recovering (DB, file system, object store).
- RPO/RTO targets are defined (or can be negotiated with the business).
- Budget exists for offsite + immutable storage.

## Skip If (ANY kills it)

- Ephemeral envs (CI runners, review apps) — rely on IaC rebuild.
- Fully regenerable data (CDN cache, build artefacts) — store source, not derivative.
- Dev DB with no real data — use seed scripts, not backups.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| RPO/RTO targets | hours | business / SLO |
| Data inventory | list of stores (DB, files, K8s PVs) | platform team |
| Compliance scope | retention period per regulation | GRC |
| Budget | $ / month for storage + tooling | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[aws-well-architected-checklists]] | Reliability pillar items are tied to BCDR posture |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 3-2-1-1-0-rule, compliance-mode-not-governance, automated-restore-test, rpo-rto-documented, skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for backup spec + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: governance-mode-deletable, no-restore-test, no-offsite, single-copy | 800 |
| `content/04-procedure.xml` | essential | 5 steps: inventory → choose media → schedule → immutable copy → restore-verify | 800 |
| `content/05-examples.xml` | reference | Worked example: PostgreSQL prod with 3-2-1-1-0 | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on RPO/RTO + compliance → strategy | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-media-and-tool` | sonnet | Strategic — cost vs RPO/RTO trade-off. |
| `compose-schedule` | haiku | Mechanical cron + retention math. |
| `design-restore-test` | sonnet | Wire the verification job. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backup-spec.md.j2` | Markdown skeleton for the backup spec |
| `templates/backup-spec.md` | Markdown skeleton for the backup spec Generated from `templates/backup-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/restic-backup.sh` | Restic backup script — production-ready bash with retention prune |
| `templates/verify-backup.sh` | Restore-verification script — restores latest snapshot to /tmp + asserts |
| `templates/_smoke-test.json` | Minimum spec used by validate-backup-strategies.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-strategies.py` | Validate the spec artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[aws-well-architected-checklists]]
- [[azure-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when designing or auditing backups for any prod stateful workload.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/restic-backup.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:?missing}"
export RESTIC_PASSWORD="${RESTIC_PASSWORD:?missing}"

TARGETS=("/var/lib/postgresql" "/etc")

restic snapshots >/dev/null 2>&1 || restic init
restic backup --tag prod "${TARGETS[@]}"
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
restic check
```

### `templates/verify-backup.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:?missing}"
export RESTIC_PASSWORD="${RESTIC_PASSWORD:?missing}"
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

restic restore latest --target "$TMP"
[[ -d "$TMP/var/lib/postgresql" ]] || { echo "FAIL: pg dir missing"; exit 1; }
echo OK
```

### `templates/_smoke-test.json`

```json
{
  "workload": "checkout-db",
  "rpo_hours": 1,
  "rto_hours": 4,
  "retention_days": 90,
  "copies": [
    {
      "media": "local-nas",
      "offsite": false,
      "immutable": false
    },
    {
      "media": "s3-standard-ia",
      "offsite": true,
      "immutable": false
    },
    {
      "media": "s3-object-lock-compliance",
      "offsite": true,
      "immutable": true,
      "lock_mode": "COMPLIANCE"
    }
  ],
  "restore_verification": {
    "cadence": "nightly",
    "method": "pg_restore-to-isolated-db",
    "last_pass": "2026-05-22"
  }
}
```
