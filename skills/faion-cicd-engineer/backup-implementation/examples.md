# Backup Implementation Examples

## Database Backups

### PostgreSQL Full Backup

```bash
#!/bin/bash
# postgres_backup.sh - PostgreSQL backup with S3 upload

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
S3_BUCKET="s3://backups-bucket/postgres"

mkdir -p "$BACKUP_DIR"

# Full backup with custom format
pg_dump -h localhost -U postgres -Fc "$DB_NAME" > \
  "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Parallel dump for large databases (4 workers)
# pg_dump -h localhost -U postgres -Fc -j 4 "$DB_NAME" > \
#   "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Upload to S3
aws s3 cp "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump" \
  "$S3_BUCKET/${DB_NAME}/" \
  --storage-class STANDARD_IA

# Cleanup old local backups
find "$BACKUP_DIR" -type f -name "*.dump" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: ${DB_NAME}_${TIMESTAMP}.dump"
```

### PostgreSQL PITR Setup

```bash
#!/bin/bash
# postgres_basebackup.sh - Base backup for Point-in-Time Recovery

set -euo pipefail

BACKUP_DIR="/var/backups/postgres/base"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create base backup with streaming WAL
pg_basebackup \
  -h localhost \
  -U replication \
  -D "$BACKUP_DIR/base_$TIMESTAMP" \
  -Ft \
  -z \
  -P \
  -X stream

echo "Base backup created: $BACKUP_DIR/base_$TIMESTAMP"
```

### MySQL/MariaDB Backup

```bash
#!/bin/bash
# mysql_backup.sh - MySQL backup with compression

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
BACKUP_DIR="/var/backups/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Full backup with mysqldump
mysqldump \
  -u root \
  -p"$MYSQL_PASSWORD" \
  --single-transaction \
  --routines \
  --triggers \
  --quick \
  "$DB_NAME" | gzip > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "Backup completed: ${DB_NAME}_${TIMESTAMP}.sql.gz"
```

### XtraBackup for Large MySQL

```bash
#!/bin/bash
# xtrabackup_full.sh - Percona XtraBackup for large databases

set -euo pipefail

BACKUP_DIR="/var/backups/mysql/xtrabackup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Full backup (no locking for InnoDB)
xtrabackup --backup \
  --target-dir="$BACKUP_DIR/full_$TIMESTAMP" \
  --user=root \
  --password="$MYSQL_PASSWORD"

# Prepare backup for restore
xtrabackup --prepare \
  --target-dir="$BACKUP_DIR/full_$TIMESTAMP"

echo "XtraBackup completed: $BACKUP_DIR/full_$TIMESTAMP"
```

### MongoDB Backup

```bash
#!/bin/bash
# mongodb_backup.sh - MongoDB backup with oplog

set -euo pipefail

BACKUP_DIR="/var/backups/mongodb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MONGO_URI="mongodb://localhost:27017"

mkdir -p "$BACKUP_DIR"

# Archive format with compression and oplog
mongodump \
  --uri="$MONGO_URI" \
  --archive="$BACKUP_DIR/backup_$TIMESTAMP.gz" \
  --oplog \
  --gzip

echo "MongoDB backup completed: backup_$TIMESTAMP.gz"
```

## File System Backups

### Restic Full Example

```bash
#!/bin/bash
# restic_backup.sh - Restic backup to S3

set -euo pipefail

export RESTIC_REPOSITORY="s3:s3.amazonaws.com/backup-bucket/restic"
export RESTIC_PASSWORD_FILE="/etc/restic/password"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"

# Initialize repository (first time only)
# restic init

# Backup with exclusions and tags
restic backup /var/www /etc /home \
  --exclude="*.log" \
  --exclude="*.tmp" \
  --exclude="node_modules" \
  --exclude=".git" \
  --exclude="__pycache__" \
  --exclude=".cache" \
  --tag production \
  --tag "$(hostname)"

# Prune old snapshots (keep 7 daily, 4 weekly, 12 monthly)
restic forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune

# Check repository integrity (weekly)
# restic check

echo "Restic backup completed"
```

### Restic Restore Examples

```bash
# List available snapshots
restic snapshots

# Restore latest snapshot to /restore
restic restore latest --target /restore

# Restore specific snapshot
restic restore abc123 --target /restore

# Restore specific files only
restic restore latest \
  --target /restore \
  --include "/var/www/config.php" \
  --include "/etc/nginx"

# Mount snapshots as filesystem (browse and recover)
restic mount /mnt/restic
```

### BorgBackup Example

```bash
#!/bin/bash
# borg_backup.sh - BorgBackup with compression

set -euo pipefail

export BORG_REPO="/backup/borg-repo"
export BORG_PASSPHRASE="${BORG_PASSPHRASE}"

# Initialize repository (first time only)
# borg init --encryption=repokey "$BORG_REPO"

# Create backup with compression
borg create \
  --stats \
  --progress \
  --compression lz4 \
  "$BORG_REPO::{hostname}-{now}" \
  /var/www \
  /etc \
  --exclude '*.log' \
  --exclude 'node_modules' \
  --exclude '.cache'

# Prune old archives
borg prune \
  --keep-daily=7 \
  --keep-weekly=4 \
  --keep-monthly=12 \
  "$BORG_REPO"

echo "Borg backup completed"
```

### Rsync Incremental Backup

```bash
#!/bin/bash
# rsync_backup.sh - Incremental backup with hard links

set -euo pipefail

SOURCE="/var/www/"
DEST_HOST="backup-server"
DEST_BASE="/backups/www"
DATE=$(date +%Y%m%d)

# Incremental backup using hard links to previous
rsync -avz --delete \
  --link-dest="$DEST_BASE/latest" \
  --exclude='*.log' \
  --exclude='cache/*' \
  --exclude='tmp/*' \
  "$SOURCE" \
  "user@$DEST_HOST:$DEST_BASE/$DATE/"

# Update 'latest' symlink
ssh "user@$DEST_HOST" "ln -snf $DEST_BASE/$DATE $DEST_BASE/latest"

echo "Rsync backup completed: $DATE"
```

## Kubernetes Backups (Velero)

### Velero Installation

```bash
# Install Velero with AWS provider
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.10.0 \
  --bucket velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero \
  --use-node-agent \
  --default-volumes-to-fs-backup
```

### Velero Backup Commands

```bash
# Create one-time backup of specific namespace
velero backup create myapp-backup \
  --include-namespaces myapp \
  --include-resources pods,deployments,services,configmaps,secrets,pvc

# Backup with label selector
velero backup create labeled-backup \
  --selector app=myapp

# Create scheduled backup
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces myapp,myapp-db \
  --ttl 720h

# List backups
velero backup get

# Describe backup details
velero backup describe myapp-backup --details

# Restore from backup
velero restore create --from-backup myapp-backup

# Restore to different namespace
velero restore create --from-backup myapp-backup \
  --namespace-mappings myapp:myapp-restored
```

## Cloud Backups

### AWS S3 Lifecycle Script

```bash
#!/bin/bash
# setup_s3_lifecycle.sh - Configure S3 bucket for backups

BUCKET="company-backups"

# Create lifecycle configuration
cat > /tmp/lifecycle.json << 'EOF'
{
  "Rules": [
    {
      "ID": "backup-lifecycle",
      "Status": "Enabled",
      "Filter": { "Prefix": "" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "NoncurrentVersionTransitions": [
        { "NoncurrentDays": 30, "StorageClass": "GLACIER" }
      ],
      "NoncurrentVersionExpiration": { "NoncurrentDays": 730 }
    }
  ]
}
EOF

# Apply lifecycle configuration
aws s3api put-bucket-lifecycle-configuration \
  --bucket "$BUCKET" \
  --lifecycle-configuration file:///tmp/lifecycle.json

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

echo "S3 lifecycle configured for $BUCKET"
```

## Backup Verification

### PostgreSQL Verification Script

```bash
#!/bin/bash
# verify_postgres_backup.sh - Test backup integrity

set -euo pipefail

BACKUP_PATH="$1"
VERIFY_DB="backup_verify_$(date +%s)"
EXPECTED_TABLES=50
ALERT_EMAIL="ops@example.com"

# Test backup file validity
if ! pg_restore -l "$BACKUP_PATH" > /dev/null 2>&1; then
    echo "ERROR: Backup file is corrupted"
    mail -s "Backup Verification Failed" "$ALERT_EMAIL" <<< "Backup file corrupted: $BACKUP_PATH"
    exit 1
fi

# Create test database
createdb "$VERIFY_DB"

# Restore backup
pg_restore -d "$VERIFY_DB" "$BACKUP_PATH"

# Verify data integrity
ACTUAL_TABLES=$(psql -d "$VERIFY_DB" -t -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'")

if [ "$ACTUAL_TABLES" -ge "$EXPECTED_TABLES" ]; then
    echo "SUCCESS: Data integrity check passed ($ACTUAL_TABLES tables)"
else
    echo "ERROR: Table count mismatch (expected: $EXPECTED_TABLES, actual: $ACTUAL_TABLES)"
    mail -s "Backup Verification Failed" "$ALERT_EMAIL" <<< "Table count mismatch"
fi

# Cleanup
dropdb "$VERIFY_DB"
```

### Restic Verification

```bash
#!/bin/bash
# verify_restic.sh - Verify Restic repository integrity

set -euo pipefail

export RESTIC_REPOSITORY="s3:s3.amazonaws.com/backup-bucket/restic"
export RESTIC_PASSWORD_FILE="/etc/restic/password"

# Check repository integrity
restic check --read-data-subset=10%

# Verify latest snapshot is recent
LATEST=$(restic snapshots --json | jq -r '.[0].time')
LATEST_EPOCH=$(date -d "$LATEST" +%s)
NOW_EPOCH=$(date +%s)
AGE_HOURS=$(( (NOW_EPOCH - LATEST_EPOCH) / 3600 ))

if [ "$AGE_HOURS" -gt 24 ]; then
    echo "WARNING: Latest backup is $AGE_HOURS hours old"
    exit 1
fi

echo "Backup verification passed. Latest backup: $AGE_HOURS hours ago"
```

## Automation

### Systemd Timer for Backups

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup service
After=network-online.target

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
Group=backup
StandardOutput=journal
StandardError=journal
```

### Cron Configuration

```bash
# /etc/cron.d/backups

# Database backups
0 2 * * * postgres /opt/scripts/backup_postgres.sh >> /var/log/backup/postgres.log 2>&1
0 3 * * * root /opt/scripts/backup_mysql.sh >> /var/log/backup/mysql.log 2>&1

# File backups (hourly)
0 * * * * root /opt/scripts/restic_backup.sh >> /var/log/backup/restic.log 2>&1

# Verification (daily at 6am)
0 6 * * * root /opt/scripts/verify_backups.sh >> /var/log/backup/verify.log 2>&1

# Cleanup (weekly on Sunday)
0 5 * * 0 root /opt/scripts/cleanup_old_backups.sh >> /var/log/backup/cleanup.log 2>&1
```

---

*Examples last updated: 2026-01*
