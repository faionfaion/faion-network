# Backup Basics Examples

## Example 1: PostgreSQL 3-2-1-1-0 Strategy

```yaml
# PostgreSQL backup configuration following 3-2-1-1-0 rule
postgresql_backup:
  database: production_db

  # Copy 1: Primary (production)
  primary:
    location: "AWS RDS us-east-1"
    type: "live database"

  # Copy 2: Local backup (same region, different AZ)
  local_backup:
    tool: "pg_dump with WAL archiving"
    location: "AWS S3 us-east-1"
    type: "object storage"
    schedule:
      full: "daily at 02:00 UTC"
      wal: "continuous"
    retention: 30_days
    encryption: "AES-256-GCM"

  # Copy 3: Offsite backup (different region)
  offsite_backup:
    location: "AWS S3 eu-west-1"
    type: "cross-region replication"
    replication: "automatic from us-east-1"
    retention: 90_days
    encryption: "AES-256-GCM"

  # +1: Immutable copy
  immutable_copy:
    location: "AWS S3 us-east-1"
    type: "S3 Object Lock (Compliance mode)"
    lock_duration: 90_days
    governance_bypass: disabled

  # 0: Verification
  verification:
    integrity_check: "daily checksum validation"
    restore_test: "weekly automated restore to staging"
    alert_on_failure: true
```

## Example 2: Multi-Tier Backup Schedule

```yaml
backup_schedule:
  tier1_critical:
    description: "Production databases, user data"
    systems:
      - postgresql_main
      - mongodb_users
      - redis_sessions
    schedule:
      full_backup: "daily 02:00 UTC"
      incremental: "every 4 hours"
      wal_archiving: "continuous"
    retention:
      hot: 7_days
      warm: 30_days
      cold: 365_days
    rpo: 1_hour
    rto: 2_hours

  tier2_important:
    description: "Application files, configs"
    systems:
      - application_servers
      - config_files
      - ssl_certificates
    schedule:
      full_backup: "weekly Sunday 03:00 UTC"
      incremental: "daily 03:00 UTC"
    retention:
      hot: 14_days
      warm: 90_days
    rpo: 24_hours
    rto: 4_hours

  tier3_standard:
    description: "Logs, development data"
    systems:
      - log_archives
      - dev_databases
      - test_environments
    schedule:
      full_backup: "weekly Sunday 04:00 UTC"
    retention:
      hot: 7_days
    rpo: 7_days
    rto: 24_hours
```

## Example 3: Disaster Recovery Scenarios

```yaml
disaster_recovery:
  rto: 4_hours
  rpo: 1_hour

  scenarios:
    database_corruption:
      detection: "Automated monitoring alert"
      priority: P1
      steps:
        - action: "Stop application writes"
          command: "kubectl scale deployment app --replicas=0"
        - action: "Identify corruption timestamp"
          command: "pg_waldump to find last good transaction"
        - action: "Restore from point-in-time"
          command: "pg_restore with PITR to timestamp"
        - action: "Verify data integrity"
          command: "Run integrity checks and compare row counts"
        - action: "Resume operations"
          command: "kubectl scale deployment app --replicas=3"

    region_outage:
      detection: "AWS Health Dashboard + CloudWatch"
      priority: P1
      steps:
        - action: "Activate DNS failover"
          command: "Route53 health check triggers automatic failover"
        - action: "Verify DR region databases"
          command: "Check RDS read replica promotion status"
        - action: "Scale DR region compute"
          command: "kubectl scale deployment app --replicas=6 --context=dr"
        - action: "Update configuration"
          command: "Apply DR-specific config maps"
        - action: "Resume operations"
          command: "Verify application health checks"

    ransomware:
      detection: "Security alert + file integrity monitoring"
      priority: P0
      steps:
        - action: "Isolate affected systems"
          command: "Network isolation via security groups"
        - action: "Identify attack vector"
          command: "Security team forensics"
        - action: "Restore from immutable backup"
          command: "Restore from S3 Object Lock protected backup"
        - action: "Security hardening"
          command: "Patch vulnerabilities, rotate credentials"
        - action: "Resume operations"
          command: "Gradual rollout with monitoring"

  testing_schedule:
    full_dr_test: quarterly
    backup_restore_test: monthly
    runbook_review: quarterly
    tabletop_exercise: semi_annually
```

## Example 4: Restic Backup Configuration

```bash
#!/bin/bash
# restic-backup.sh - Daily backup script

# Environment
export RESTIC_REPOSITORY="s3:s3.amazonaws.com/company-backups"
export RESTIC_PASSWORD_FILE="/etc/restic/password"
export AWS_ACCESS_KEY_ID="backup-user-key"
export AWS_SECRET_ACCESS_KEY_FILE="/etc/restic/aws-secret"

# Backup databases
pg_dump production_db | restic backup --stdin --stdin-filename postgresql.sql

# Backup application files
restic backup \
  /var/www/app \
  /etc/nginx \
  /etc/ssl/certs \
  --exclude-caches \
  --exclude="*.log" \
  --exclude="*.tmp"

# Apply retention policy (keep 7 daily, 4 weekly, 12 monthly)
restic forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune

# Verify backup integrity
restic check

# Copy to secondary location (offsite)
restic copy --to-repo "s3:s3.eu-west-1.amazonaws.com/company-backups-dr"
```

## Example 5: Kubernetes Velero Backup

```yaml
# velero-schedule.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-cluster-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # Daily at 02:00 UTC
  template:
    includedNamespaces:
      - production
      - staging
    excludedResources:
      - events
      - pods
    storageLocation: default
    volumeSnapshotLocations:
      - default
    ttl: 720h  # 30 days retention
    hooks:
      resources:
        - name: postgresql-backup
          includedNamespaces:
            - production
          labelSelector:
            matchLabels:
              app: postgresql
          pre:
            - exec:
                container: postgresql
                command:
                  - /bin/sh
                  - -c
                  - pg_dump -U postgres production > /backup/pre-backup.sql
          post:
            - exec:
                container: postgresql
                command:
                  - /bin/sh
                  - -c
                  - rm /backup/pre-backup.sql
---
# Immutable backup to separate bucket
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: immutable-backup
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: company-backups-immutable
  config:
    region: us-east-1
    s3ForcePathStyle: "true"
  # S3 Object Lock configured at bucket level
```

## Example 6: SaaS Backup Strategy

```yaml
saas_backup_strategy:
  google_workspace:
    tool: "Backupify or SysCloud"
    scope:
      - Gmail
      - Drive
      - Calendar
      - Contacts
    schedule: "every 6 hours"
    retention: 2_years
    compliance: "GDPR data residency"

  microsoft_365:
    tool: "Veeam for M365 or AvePoint"
    scope:
      - Exchange Online
      - OneDrive
      - SharePoint
      - Teams
    schedule: "every 4 hours"
    retention: 7_years  # Financial compliance

  salesforce:
    tool: "OwnBackup or Odaseva"
    scope:
      - All objects and metadata
      - Files and attachments
      - Chatter data
    schedule: "daily"
    retention: 5_years
    sandbox_seeding: enabled

  github_repos:
    tool: "GitProtect or native export"
    scope:
      - All repositories
      - Issues and PRs
      - Actions workflows
      - Secrets (encrypted export)
    schedule: "daily"
    retention: 1_year
```

## Example 7: Backup Monitoring Dashboard

```yaml
# Grafana dashboard configuration
backup_monitoring:
  metrics:
    backup_success_rate:
      query: |
        sum(backup_job_success_total) /
        sum(backup_job_total) * 100
      threshold:
        warning: 95
        critical: 90

    backup_duration_seconds:
      query: |
        histogram_quantile(0.95,
          rate(backup_duration_seconds_bucket[24h]))
      threshold:
        warning: 3600   # 1 hour
        critical: 7200  # 2 hours

    backup_size_bytes:
      query: |
        sum(backup_size_bytes) by (system)
      alert_on: "unexpected growth > 20%"

    last_successful_backup:
      query: |
        time() - max(backup_last_success_timestamp)
      threshold:
        warning: 86400   # 24 hours
        critical: 172800 # 48 hours

    restore_test_success:
      query: |
        restore_test_success_total /
        restore_test_total * 100
      threshold:
        critical: 100  # Must be 100%

  alerts:
    - name: "Backup Failed"
      condition: "backup_job_success == 0"
      severity: critical
      notification: pagerduty

    - name: "Backup Overdue"
      condition: "last_successful_backup > threshold"
      severity: warning
      notification: slack

    - name: "Storage Approaching Limit"
      condition: "backup_storage_used / backup_storage_total > 0.8"
      severity: warning
      notification: email
```

---

*Backup Basics Examples | faion-cicd-engineer*
