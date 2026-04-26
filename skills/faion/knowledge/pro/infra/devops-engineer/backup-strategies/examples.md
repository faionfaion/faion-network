# Backup Strategies Examples

Working scripts and configurations for implementing backup solutions.

## Database Backups

### PostgreSQL

```bash
#!/bin/bash
# postgres_backup.sh - PostgreSQL backup with 3-2-1 rule

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
BACKUP_DIR="/var/backups/postgres"
S3_BUCKET="s3://backups-bucket/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Full backup with pg_dump (compressed custom format)
echo "Starting backup of $DB_NAME..."
pg_dump -h localhost -U postgres -Fc "$DB_NAME" > \
  "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Calculate checksum for integrity
sha256sum "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump" > \
  "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sha256"

# Upload to S3 (offsite copy)
aws s3 cp "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump" \
  "$S3_BUCKET/${DB_NAME}/" \
  --storage-class STANDARD_IA

aws s3 cp "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sha256" \
  "$S3_BUCKET/${DB_NAME}/"

# Upload to immutable storage (S3 Object Lock)
aws s3 cp "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump" \
  "s3://immutable-backups/postgres/${DB_NAME}/" \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "$(date -d '+90 days' --iso-8601=seconds)"

# Cleanup old local backups
find "$BACKUP_DIR" -type f -mtime +"$RETENTION_DAYS" -delete

echo "Backup completed: ${DB_NAME}_${TIMESTAMP}.dump"
```

### PostgreSQL PITR (Point-in-Time Recovery)

```bash
#!/bin/bash
# postgres_pitr_backup.sh - Base backup for PITR

set -euo pipefail

BACKUP_DIR="/var/backups/postgres/base"
WAL_ARCHIVE="/var/backups/postgres/wal"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create directories
mkdir -p "$BACKUP_DIR" "$WAL_ARCHIVE"

# Base backup with streaming WAL
pg_basebackup \
  -h localhost \
  -U replication \
  -D "$BACKUP_DIR/base_$TIMESTAMP" \
  -Ft \
  -z \
  -P \
  -X stream \
  --checkpoint=fast

# Configure WAL archiving in postgresql.conf:
# archive_mode = on
# archive_command = 'cp %p /var/backups/postgres/wal/%f'
# archive_timeout = 300

echo "Base backup completed: base_$TIMESTAMP"
```

### MySQL/MariaDB

```bash
#!/bin/bash
# mysql_backup.sh - MySQL backup with XtraBackup

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
BACKUP_DIR="/var/backups/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MYSQL_PASSWORD="${MYSQL_ROOT_PASSWORD}"

mkdir -p "$BACKUP_DIR"

# Full backup with mysqldump (for small databases)
mysqldump \
  -u root \
  -p"$MYSQL_PASSWORD" \
  --single-transaction \
  --routines \
  --triggers \
  --quick \
  --set-gtid-purged=OFF \
  "$DB_NAME" | gzip > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

# For large databases, use XtraBackup
# Full backup
xtrabackup \
  --backup \
  --target-dir="$BACKUP_DIR/full_$TIMESTAMP" \
  --user=root \
  --password="$MYSQL_PASSWORD" \
  --parallel=4

# Prepare backup for restore
xtrabackup \
  --prepare \
  --target-dir="$BACKUP_DIR/full_$TIMESTAMP"

echo "Backup completed: ${DB_NAME}_${TIMESTAMP}"
```

### MySQL Incremental Backup

```bash
#!/bin/bash
# mysql_incremental.sh - Incremental backup with XtraBackup

BACKUP_DIR="/var/backups/mysql"
BASE_DIR="$BACKUP_DIR/full_latest"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Incremental backup
xtrabackup \
  --backup \
  --target-dir="$BACKUP_DIR/inc_$TIMESTAMP" \
  --incremental-basedir="$BASE_DIR" \
  --user=root \
  --password="$MYSQL_ROOT_PASSWORD"

# To restore incremental:
# 1. Prepare base: xtrabackup --prepare --apply-log-only --target-dir=full_backup
# 2. Apply incremental: xtrabackup --prepare --apply-log-only --target-dir=full_backup --incremental-dir=inc_backup
# 3. Final prepare: xtrabackup --prepare --target-dir=full_backup
# 4. Restore: xtrabackup --copy-back --target-dir=full_backup
```

### MongoDB

```bash
#!/bin/bash
# mongodb_backup.sh - MongoDB backup with oplog

set -euo pipefail

BACKUP_DIR="/var/backups/mongodb"
MONGO_URI="${MONGO_URI:-mongodb://localhost:27017}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
S3_BUCKET="s3://backups-bucket/mongodb"

mkdir -p "$BACKUP_DIR"

# Dump with oplog for PITR (replica set only)
mongodump \
  --uri="$MONGO_URI" \
  --archive="$BACKUP_DIR/backup_$TIMESTAMP.gz" \
  --gzip \
  --oplog

# Upload to S3
aws s3 cp "$BACKUP_DIR/backup_$TIMESTAMP.gz" "$S3_BUCKET/"

# Cleanup local (keep 7 days)
find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "MongoDB backup completed: backup_$TIMESTAMP.gz"
```

## File System Backups

### Restic with S3

```bash
#!/bin/bash
# restic_backup.sh - Restic backup to S3 with encryption

set -euo pipefail

export RESTIC_REPOSITORY="s3:s3.amazonaws.com/backup-bucket/restic"
export RESTIC_PASSWORD_FILE="/etc/restic/password"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"

# Initialize repository (first time only)
# restic init

# Backup with exclusions
restic backup \
  /var/www \
  /etc \
  /home \
  --exclude="*.log" \
  --exclude="node_modules" \
  --exclude=".git" \
  --exclude="__pycache__" \
  --exclude=".cache" \
  --tag production \
  --tag "$(hostname)" \
  --verbose

# Prune old backups (3-2-1 retention)
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --keep-yearly 2 \
  --prune

# Check repository integrity
restic check

echo "Restic backup completed"
```

### Restic Restore

```bash
#!/bin/bash
# restic_restore.sh - Restore from Restic

export RESTIC_REPOSITORY="s3:s3.amazonaws.com/backup-bucket/restic"
export RESTIC_PASSWORD_FILE="/etc/restic/password"

# List snapshots
restic snapshots

# Restore latest
restic restore latest \
  --target /restore \
  --include "/var/www"

# Restore specific snapshot
# restic restore abc123 --target /restore

# Restore specific files
restic restore latest \
  --target /restore \
  --include "/var/www/config.php" \
  --include "/etc/nginx"

# Mount for browsing (interactive)
# restic mount /mnt/restic
```

### BorgBackup

```bash
#!/bin/bash
# borg_backup.sh - BorgBackup with encryption and compression

set -euo pipefail

export BORG_REPO="/backup/borg-repo"
export BORG_PASSPHRASE="${BORG_PASSPHRASE}"

# Initialize (first time)
# borg init --encryption=repokey-blake2 "$BORG_REPO"

# Create backup
borg create \
  --stats \
  --progress \
  --compression zstd,5 \
  --exclude '*.log' \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude '__pycache__' \
  "${BORG_REPO}::{hostname}-{now}" \
  /var/www \
  /etc \
  /home

# Prune old backups
borg prune \
  --keep-hourly=24 \
  --keep-daily=7 \
  --keep-weekly=4 \
  --keep-monthly=12 \
  "${BORG_REPO}"

# Compact repository
borg compact "${BORG_REPO}"

echo "Borg backup completed"
```

### Rsync Incremental

```bash
#!/bin/bash
# rsync_incremental.sh - Incremental backup with hard links

set -euo pipefail

SOURCE="/var/www"
DEST_HOST="backup-server"
DEST_BASE="/backups/www"
DATE=$(date +%Y%m%d)

# Create incremental backup with hard links to previous
rsync -avz \
  --delete \
  --link-dest="${DEST_BASE}/latest" \
  --exclude='*.log' \
  --exclude='cache/*' \
  --exclude='tmp/*' \
  "${SOURCE}/" \
  "${DEST_HOST}:${DEST_BASE}/${DATE}/"

# Update 'latest' symlink
ssh "${DEST_HOST}" "ln -snf ${DEST_BASE}/${DATE} ${DEST_BASE}/latest"

# Cleanup old backups (keep 30 days)
ssh "${DEST_HOST}" "find ${DEST_BASE} -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;"

echo "Rsync backup completed: $DATE"
```

## Kubernetes Backups

### Velero Installation

```bash
#!/bin/bash
# velero_install.sh - Install Velero with AWS plugin

# Install Velero CLI
wget https://github.com/vmware-tanzu/velero/releases/download/v1.12.0/velero-v1.12.0-linux-amd64.tar.gz
tar -xvf velero-v1.12.0-linux-amd64.tar.gz
sudo mv velero-v1.12.0-linux-amd64/velero /usr/local/bin/

# Create credentials file
cat > /tmp/credentials-velero << EOF
[default]
aws_access_key_id=${AWS_ACCESS_KEY_ID}
aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}
EOF

# Install Velero in cluster
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file /tmp/credentials-velero \
  --use-volume-snapshots=true \
  --default-volumes-to-fs-backup

rm /tmp/credentials-velero
```

### Velero Backup Schedule

```yaml
# velero-schedule.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  template:
    includedNamespaces:
      - production
      - staging
    excludedResources:
      - events
      - events.events.k8s.io
    storageLocation: default
    volumeSnapshotLocations:
      - default
    ttl: 720h  # 30 days
    snapshotVolumes: true
    defaultVolumesToFsBackup: true
---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: weekly-backup
  namespace: velero
spec:
  schedule: "0 3 * * 0"  # Weekly on Sunday at 3 AM
  template:
    includedNamespaces:
      - production
    ttl: 2160h  # 90 days
    snapshotVolumes: true
```

### Velero Backup Commands

```bash
#!/bin/bash
# velero_operations.sh - Common Velero operations

# Create manual backup
velero backup create manual-backup-$(date +%Y%m%d) \
  --include-namespaces production \
  --wait

# List backups
velero backup get

# Describe backup
velero backup describe manual-backup-20240115

# View backup logs
velero backup logs manual-backup-20240115

# Restore from backup
velero restore create --from-backup manual-backup-20240115

# Restore to different namespace
velero restore create --from-backup manual-backup-20240115 \
  --namespace-mappings production:production-restored

# Delete backup
velero backup delete manual-backup-20240115

# Check Velero status
velero get backup-locations
velero get snapshot-locations
```

## Cloud Backups

### AWS Backup with Terraform

```hcl
# aws_backup.tf

resource "aws_backup_vault" "main" {
  name        = "main-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn

  tags = {
    Environment = "production"
  }
}

# Immutable vault (cannot delete backups)
resource "aws_backup_vault_lock_configuration" "main" {
  backup_vault_name   = aws_backup_vault.main.name
  min_retention_days  = 7
  max_retention_days  = 365
  changeable_for_days = 3  # Grace period
}

resource "aws_backup_plan" "comprehensive" {
  name = "comprehensive-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }

    # Cross-region copy for DR
    copy_action {
      destination_vault_arn = aws_backup_vault.dr_region.arn
      lifecycle {
        cold_storage_after = 30
        delete_after       = 365
      }
    }
  }

  rule {
    rule_name         = "weekly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 3 ? * SUN *)"

    lifecycle {
      cold_storage_after = 90
      delete_after       = 730
    }
  }

  rule {
    rule_name         = "monthly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 4 1 * ? *)"

    lifecycle {
      cold_storage_after = 180
      delete_after       = 2555  # 7 years
    }
  }
}

resource "aws_backup_selection" "all_tagged" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "all-tagged-resources"
  plan_id      = aws_backup_plan.comprehensive.id

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}
```

### S3 Immutable Backup Bucket

```hcl
# s3_immutable.tf

resource "aws_s3_bucket" "immutable_backups" {
  bucket = "company-immutable-backups"
}

resource "aws_s3_bucket_versioning" "immutable_backups" {
  bucket = aws_s3_bucket.immutable_backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable Object Lock (must be set at bucket creation)
resource "aws_s3_bucket_object_lock_configuration" "immutable_backups" {
  bucket = aws_s3_bucket.immutable_backups.id

  rule {
    default_retention {
      mode = "COMPLIANCE"  # Cannot be overridden, even by root
      days = 90
    }
  }
}

# Lifecycle for cost optimization
resource "aws_s3_bucket_lifecycle_configuration" "immutable_backups" {
  bucket = aws_s3_bucket.immutable_backups.id

  rule {
    id     = "archive-old-backups"
    status = "Enabled"

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
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "immutable_backups" {
  bucket = aws_s3_bucket.immutable_backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## Backup Verification

### Automated Verification Script

```bash
#!/bin/bash
# verify_backup.sh - Automated backup verification

set -euo pipefail

BACKUP_PATH="$1"
DB_NAME="${2:-backup_test}"
VERIFY_DIR="/tmp/backup_verify_$$"
ALERT_EMAIL="ops@example.com"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"

cleanup() {
  rm -rf "$VERIFY_DIR"
  psql -c "DROP DATABASE IF EXISTS $DB_NAME" 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$VERIFY_DIR"

send_alert() {
  local message="$1"
  local severity="${2:-error}"

  # Email alert
  echo "$message" | mail -s "Backup Verification: $severity" "$ALERT_EMAIL"

  # Slack alert
  if [[ -n "$SLACK_WEBHOOK" ]]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"Backup Verification ($severity): $message\"}" \
      "$SLACK_WEBHOOK"
  fi
}

echo "Testing backup: $BACKUP_PATH"

# Verify backup file exists and is not empty
if [[ ! -f "$BACKUP_PATH" ]] || [[ ! -s "$BACKUP_PATH" ]]; then
  send_alert "Backup file missing or empty: $BACKUP_PATH" "critical"
  exit 1
fi

# Verify backup format (PostgreSQL)
if ! pg_restore -l "$BACKUP_PATH" > /dev/null 2>&1; then
  send_alert "Backup file corrupted: $BACKUP_PATH" "critical"
  exit 1
fi

echo "Backup file is valid, testing restore..."

# Create test database
psql -c "CREATE DATABASE $DB_NAME"

# Restore to test database
START_TIME=$(date +%s)
pg_restore -d "$DB_NAME" "$BACKUP_PATH" 2>&1 || true
END_TIME=$(date +%s)
RESTORE_TIME=$((END_TIME - START_TIME))

echo "Restore completed in ${RESTORE_TIME}s"

# Verify data integrity
EXPECTED_TABLES=50  # Adjust based on your schema
ACTUAL_TABLES=$(psql -d "$DB_NAME" -t -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'")

if [[ "$ACTUAL_TABLES" -lt "$EXPECTED_TABLES" ]]; then
  send_alert "Table count mismatch: expected $EXPECTED_TABLES, got $ACTUAL_TABLES" "warning"
  exit 1
fi

# Check for recent data
RECENT_RECORDS=$(psql -d "$DB_NAME" -t -c \
  "SELECT count(*) FROM audit_log WHERE created_at > NOW() - INTERVAL '24 hours'" 2>/dev/null || echo "0")

echo "Verification passed:"
echo "  - Tables: $ACTUAL_TABLES"
echo "  - Restore time: ${RESTORE_TIME}s"
echo "  - Recent records: $RECENT_RECORDS"

# Log success metric
echo "backup_verification_success 1" | curl --data-binary @- \
  http://pushgateway:9091/metrics/job/backup_verify/instance/"$(hostname)"
```

## Monitoring

### Prometheus Alerts

```yaml
# prometheus-backup-rules.yaml
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
          description: "Last successful backup for {{ $labels.job }} was {{ humanizeTimestamp $value }}"

      - alert: BackupFailed
        expr: backup_last_status == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Backup job failed"
          description: "Backup job {{ $labels.job }} failed"

      - alert: BackupSizeAnomaly
        expr: |
          abs(backup_size_bytes - backup_size_bytes offset 1d)
          / backup_size_bytes offset 1d > 0.5
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Backup size changed by more than 50%"
          description: "Backup size for {{ $labels.job }} changed significantly"

      - alert: BackupStorageLow
        expr: backup_storage_free_bytes / backup_storage_total_bytes < 0.2
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Backup storage below 20%"
          description: "Backup storage at {{ humanizePercentage $value }}"

      - alert: BackupVerificationFailed
        expr: backup_verification_success == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Backup verification failed"
          description: "Could not restore and verify backup for {{ $labels.job }}"
```

### Cron Schedule

```bash
# /etc/cron.d/backups

# Database backups
0 2 * * * postgres /opt/scripts/postgres_backup.sh >> /var/log/backup/postgres.log 2>&1
0 3 * * * mysql /opt/scripts/mysql_backup.sh >> /var/log/backup/mysql.log 2>&1
0 4 * * * mongodb /opt/scripts/mongodb_backup.sh >> /var/log/backup/mongodb.log 2>&1

# File backups (hourly)
0 * * * * root /opt/scripts/restic_backup.sh >> /var/log/backup/restic.log 2>&1

# Weekly full backup
0 1 * * 0 root /opt/scripts/weekly_full_backup.sh >> /var/log/backup/weekly.log 2>&1

# Backup verification (daily)
0 6 * * * root /opt/scripts/verify_backup.sh /var/backups/postgres/latest.dump >> /var/log/backup/verify.log 2>&1

# Cleanup old backups
0 5 * * * root /opt/scripts/cleanup_backups.sh >> /var/log/backup/cleanup.log 2>&1

# Monthly DR test
0 2 1 * * root /opt/scripts/dr_test.sh >> /var/log/backup/dr_test.log 2>&1
```
