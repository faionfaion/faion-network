#!/bin/bash
# postgres-backup.sh — PostgreSQL backup with S3 + S3 Object Lock immutable copy
# Usage: DB_NAME=mydb S3_BUCKET=s3://bucket IMMUTABLE_BUCKET=s3://imm-bucket ./postgres-backup.sh

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/postgres}"
S3_BUCKET="${S3_BUCKET:-s3://backups-bucket/postgres}"
IMMUTABLE_BUCKET="${IMMUTABLE_BUCKET:-s3://immutable-backups/postgres}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS="${RETENTION_DAYS:-30}"

mkdir -p "$BACKUP_DIR"

echo "[$(date -Iseconds)] Starting backup of $DB_NAME"

BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Full backup (compressed custom format)
pg_dump -h localhost -U postgres -Fc "$DB_NAME" > "$BACKUP_FILE"

# Checksum for integrity verification
sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"

# Offsite copy (Standard-IA for cost)
aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/${DB_NAME}/" --storage-class STANDARD_IA
aws s3 cp "${BACKUP_FILE}.sha256" "$S3_BUCKET/${DB_NAME}/"

# Immutable copy (COMPLIANCE mode — cannot be deleted even by root)
aws s3 cp "$BACKUP_FILE" "$IMMUTABLE_BUCKET/${DB_NAME}/" \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "$(date -d "+${RETENTION_DAYS} days" --iso-8601=seconds)"

# Cleanup local backups older than retention period
find "$BACKUP_DIR" -type f -mtime +"$RETENTION_DAYS" -delete

echo "[$(date -Iseconds)] Backup completed: ${DB_NAME}_${TIMESTAMP}.dump"
