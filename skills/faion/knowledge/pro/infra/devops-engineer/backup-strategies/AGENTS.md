# Backup Strategies

## Summary

Modern backup strategy follows the 3-2-1-1-0 rule: 3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 verified recovery errors. The zero-error component is mandatory — untested backups do not count. Implement automated restore verification after every backup job.

## Why

The traditional 3-2-1 rule fails against ransomware because all three copies can be on network-reachable storage. The additional "1 immutable" copy (S3 Object Lock COMPLIANCE mode, Azure Immutable Blob, WORM tape) cannot be deleted or encrypted even by admin credentials. The "0 errors" component catches silent corruption and restores that fail only when needed most.

## When To Use

- Any production database, file system, or Kubernetes cluster requires DR capability
- Compliance requirements mandate data retention (GDPR, HIPAA, SOC2, PCI-DSS)
- RPO &lt; 24 hours is a business requirement
- Ransomware protection is part of the security posture

## When NOT To Use

- Ephemeral environments (CI runners, short-lived review apps) — backup overhead exceeds value; rely on infrastructure-as-code rebuild instead
- Data that can be fully regenerated from source (build artifacts, CDN caches) — store source, not derivatives
- Development databases with no production data — use database seeding scripts instead of backups

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategy.xml` | 3-2-1-1-0 rule, immutable storage options, RPO/RTO tiers, tool selection by target |
| `content/02-implementation.xml` | PostgreSQL PITR, MySQL XtraBackup, MongoDB oplog, Restic/BorgBackup/Velero patterns, verification |

## Templates

| File | Purpose |
|------|---------|
| `templates/postgres-backup.sh` | PostgreSQL pg_dump with S3 + immutable upload + checksum |
| `templates/restic-backup.sh` | Restic backup to S3 with retention pruning and integrity check |
| `templates/velero-schedule.yaml` | Velero daily/weekly backup schedule with TTL |
| `templates/aws-backup.tf` | Terraform AWS Backup vault + plan with vault lock + cross-region copy |
| `templates/verify-backup.sh` | Automated PostgreSQL restore verification with alerting |
| `templates/backup-policy.md` | Backup policy document template (RPO/RTO, schedule, contacts) |
| `templates/prometheus-alerts.yaml` | Prometheus alerting rules for backup age, failure, size anomaly |
