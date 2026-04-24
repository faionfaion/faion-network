# Backup Implementation Templates

## Terraform Templates

### AWS Backup Vault and Plan

```hcl
# aws_backup.tf - Complete AWS Backup configuration

resource "aws_backup_vault" "main" {
  name        = "${var.project}-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_backup_vault" "dr_region" {
  provider    = aws.dr_region
  name        = "${var.project}-backup-vault-dr"
  kms_key_arn = aws_kms_key.backup_dr.arn

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_backup_plan" "daily" {
  name = "${var.project}-daily-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"
    start_window      = 60
    completion_window = 180

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr_region.arn
      lifecycle {
        delete_after = 365
      }
    }
  }

  rule {
    rule_name         = "weekly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 ? * SUN *)"
    start_window      = 60
    completion_window = 300

    lifecycle {
      cold_storage_after = 90
      delete_after       = 730
    }
  }

  rule {
    rule_name         = "monthly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 1 * ? *)"
    start_window      = 60
    completion_window = 360

    lifecycle {
      cold_storage_after = 90
      delete_after       = 2555  # 7 years
    }
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_backup_selection" "databases" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "${var.project}-database-selection"
  plan_id      = aws_backup_plan.daily.id

  resources = [
    "arn:aws:rds:*:${data.aws_caller_identity.current.account_id}:db:*",
    "arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/*"
  ]

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}

resource "aws_iam_role" "backup" {
  name = "${var.project}-backup-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "backup.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_iam_role_policy_attachment" "restore" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}
```

### S3 Backup Bucket with Lifecycle

```hcl
# s3_backup_bucket.tf - S3 bucket for backups with lifecycle rules

resource "aws_s3_bucket" "backups" {
  bucket = "${var.project}-backups-${var.environment}"

  tags = {
    Environment = var.environment
    Purpose     = "Backups"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.backup.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "backup-lifecycle"
    status = "Enabled"

    filter {
      prefix = ""
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 730
    }
  }
}

resource "aws_s3_bucket_replication_configuration" "backups" {
  count  = var.enable_cross_region_replication ? 1 : 0
  bucket = aws_s3_bucket.backups.id
  role   = aws_iam_role.replication.arn

  rule {
    id     = "cross-region-replication"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.backups_dr.arn
      storage_class = "STANDARD_IA"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "backups" {
  bucket = aws_s3_bucket.backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Object Lock for immutable backups (ransomware protection)
resource "aws_s3_bucket_object_lock_configuration" "backups" {
  count  = var.enable_object_lock ? 1 : 0
  bucket = aws_s3_bucket.backups.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 30
    }
  }
}
```

## Kubernetes Templates

### Velero Backup CRD

```yaml
# velero-backup.yaml - Backup resource definition
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: myapp-backup
  namespace: velero
  labels:
    app.kubernetes.io/name: velero-backup
    app.kubernetes.io/component: backup
spec:
  # Namespaces to include
  includedNamespaces:
    - myapp
    - myapp-db

  # Resources to include
  includedResources:
    - pods
    - deployments
    - replicasets
    - services
    - configmaps
    - secrets
    - persistentvolumeclaims
    - ingresses

  # Resources to exclude
  excludedResources:
    - events
    - nodes

  # Label selector (optional)
  labelSelector:
    matchLabels:
      backup: "true"

  # Storage location
  storageLocation: default

  # Volume snapshot locations
  volumeSnapshotLocations:
    - default

  # TTL for this backup
  ttl: 720h0m0s

  # Snapshot volumes
  snapshotVolumes: true

  # Use Kopia for FSB (not Restic - deprecated)
  defaultVolumesToFsBackup: false
```

### Velero Schedule CRD

```yaml
# velero-schedule.yaml - Scheduled backup definition
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 2 AM daily

  template:
    includedNamespaces:
      - myapp
      - myapp-db

    includedResources:
      - "*"

    excludedResources:
      - events

    storageLocation: default

    volumeSnapshotLocations:
      - default

    ttl: 720h0m0s  # 30 days

    snapshotVolumes: true

---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: weekly-backup
  namespace: velero
spec:
  schedule: "0 3 * * 0"  # 3 AM Sunday

  template:
    includedNamespaces:
      - "*"

    excludedNamespaces:
      - kube-system
      - velero

    storageLocation: default

    ttl: 2160h0m0s  # 90 days
```

### Velero BackupStorageLocation

```yaml
# velero-bsl.yaml - Backup storage location for AWS S3
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-backups
    prefix: cluster-prod
  config:
    region: us-east-1
    s3ForcePathStyle: "false"
    s3Url: ""
  credential:
    name: velero-aws-credentials
    key: cloud
  accessMode: ReadWrite
  default: true
```

## Prometheus Monitoring Templates

### Backup Alerting Rules

```yaml
# prometheus-backup-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: backup-alerts
  namespace: monitoring
spec:
  groups:
    - name: backup-alerts
      rules:
        - alert: BackupNotRecent
          expr: time() - backup_last_success_timestamp > 86400
          for: 1h
          labels:
            severity: critical
          annotations:
            summary: "Backup is more than 24 hours old"
            description: "Backup {{ $labels.job }} last succeeded {{ humanizeTimestamp $value }} ago"

        - alert: BackupFailed
          expr: backup_last_status == 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Backup job failed"
            description: "Backup {{ $labels.job }} has failed"

        - alert: BackupSizeDrop
          expr: |
            (backup_size_bytes - backup_size_bytes offset 1d)
            / backup_size_bytes offset 1d < -0.5
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: "Backup size dropped by more than 50%"
            description: "Backup {{ $labels.job }} size decreased significantly"

        - alert: BackupDurationIncreased
          expr: |
            backup_duration_seconds >
            (avg_over_time(backup_duration_seconds[7d]) * 2)
          for: 30m
          labels:
            severity: warning
          annotations:
            summary: "Backup duration doubled"
            description: "Backup {{ $labels.job }} taking longer than usual"

        - alert: VeleroBackupFailed
          expr: |
            increase(velero_backup_failure_total[1h]) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Velero backup failed"
            description: "Velero backup in namespace {{ $labels.namespace }} failed"

        - alert: VeleroBackupPartiallyFailed
          expr: |
            increase(velero_backup_partial_failure_total[1h]) > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Velero backup partially failed"
            description: "Some items in Velero backup failed"
```

### Grafana Dashboard JSON

```json
{
  "title": "Backup Monitoring",
  "panels": [
    {
      "title": "Backup Success Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "avg(backup_last_status) * 100",
          "legendFormat": "Success Rate"
        }
      ]
    },
    {
      "title": "Last Backup Age (hours)",
      "type": "gauge",
      "targets": [
        {
          "expr": "(time() - backup_last_success_timestamp) / 3600",
          "legendFormat": "{{ job }}"
        }
      ]
    },
    {
      "title": "Backup Size Trend",
      "type": "graph",
      "targets": [
        {
          "expr": "backup_size_bytes",
          "legendFormat": "{{ job }}"
        }
      ]
    },
    {
      "title": "Backup Duration",
      "type": "graph",
      "targets": [
        {
          "expr": "backup_duration_seconds",
          "legendFormat": "{{ job }}"
        }
      ]
    }
  ]
}
```

## Script Templates

### Generic Backup Script Template

```bash
#!/bin/bash
# backup_template.sh - Generic backup script template

set -euo pipefail

# Configuration
BACKUP_NAME="${BACKUP_NAME:-mybackup}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
S3_BUCKET="${S3_BUCKET:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/backup/${BACKUP_NAME}.log"

# Metrics (for Prometheus pushgateway)
METRICS_URL="${METRICS_URL:-}"
JOB_NAME="backup_${BACKUP_NAME}"

# Functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

push_metrics() {
    if [[ -n "$METRICS_URL" ]]; then
        cat <<EOF | curl --data-binary @- "$METRICS_URL/metrics/job/$JOB_NAME"
backup_last_status $1
backup_last_success_timestamp $(date +%s)
backup_size_bytes $2
backup_duration_seconds $3
EOF
    fi
}

cleanup_old() {
    find "$BACKUP_DIR" -name "${BACKUP_NAME}_*.gz" -mtime +$RETENTION_DAYS -delete
}

# Main
main() {
    local start_time=$(date +%s)
    local status=1
    local size=0

    log "Starting backup: $BACKUP_NAME"
    mkdir -p "$BACKUP_DIR"

    # TODO: Replace with actual backup command
    # Example: pg_dump, mysqldump, tar, restic, etc.
    #
    # backup_file="$BACKUP_DIR/${BACKUP_NAME}_${TIMESTAMP}.gz"
    # your_backup_command | gzip > "$backup_file"

    if [[ $? -eq 0 ]]; then
        status=1
        # size=$(stat -f%z "$backup_file" 2>/dev/null || stat -c%s "$backup_file")
        log "Backup completed successfully"

        # Upload to S3 if configured
        if [[ -n "$S3_BUCKET" ]]; then
            aws s3 cp "$backup_file" "$S3_BUCKET/"
            log "Uploaded to S3: $S3_BUCKET"
        fi
    else
        status=0
        log "ERROR: Backup failed"
    fi

    cleanup_old

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    push_metrics $status $size $duration
    log "Duration: ${duration}s"

    exit $((1 - status))
}

main "$@"
```

### Restic Wrapper Script

```bash
#!/bin/bash
# restic_wrapper.sh - Restic backup with monitoring

set -euo pipefail

# Load configuration
source /etc/restic/config

# Required: RESTIC_REPOSITORY, RESTIC_PASSWORD_FILE
# Optional: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

BACKUP_PATHS="${BACKUP_PATHS:-/var/www /etc}"
EXCLUDE_FILE="/etc/restic/excludes"
RETENTION_DAILY="${RETENTION_DAILY:-7}"
RETENTION_WEEKLY="${RETENTION_WEEKLY:-4}"
RETENTION_MONTHLY="${RETENTION_MONTHLY:-12}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Backup
log "Starting Restic backup"
restic backup $BACKUP_PATHS \
    --exclude-file="$EXCLUDE_FILE" \
    --tag "$(hostname)" \
    --tag "scheduled"

# Forget old snapshots
log "Pruning old snapshots"
restic forget \
    --keep-daily "$RETENTION_DAILY" \
    --keep-weekly "$RETENTION_WEEKLY" \
    --keep-monthly "$RETENTION_MONTHLY" \
    --prune

# Weekly integrity check
if [[ $(date +%u) -eq 7 ]]; then
    log "Running weekly integrity check"
    restic check --read-data-subset=5%
fi

log "Backup completed"
```

## Docker Compose Template

### Backup Service Stack

```yaml
# docker-compose.backup.yaml
version: '3.8'

services:
  backup-scheduler:
    image: mcuadros/ofelia:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./ofelia.ini:/etc/ofelia/config.ini:ro
    restart: unless-stopped

  restic-backup:
    image: restic/restic:latest
    volumes:
      - /var/www:/data/www:ro
      - /etc:/data/etc:ro
      - ./restic-password:/restic-password:ro
    environment:
      - RESTIC_REPOSITORY=s3:s3.amazonaws.com/backup-bucket
      - RESTIC_PASSWORD_FILE=/restic-password
      - AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY
    entrypoint: ["restic"]
    command: ["backup", "/data", "--tag", "docker"]

  postgres-backup:
    image: postgres:15
    environment:
      - PGHOST=postgres
      - PGUSER=backup
      - PGPASSWORD_FILE=/run/secrets/pg_password
    volumes:
      - backup-data:/backups
      - ./backup-postgres.sh:/backup.sh:ro
    secrets:
      - pg_password
    entrypoint: ["/backup.sh"]

volumes:
  backup-data:

secrets:
  pg_password:
    file: ./secrets/pg_password
```

---

*Templates last updated: 2026-01*
