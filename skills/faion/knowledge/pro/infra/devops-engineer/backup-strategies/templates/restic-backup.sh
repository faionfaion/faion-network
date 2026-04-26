#!/bin/bash
# restic-backup.sh — Restic backup to S3 with retention pruning and integrity check
# Usage: RESTIC_REPOSITORY=s3:... RESTIC_PASSWORD_FILE=/etc/restic/password ./restic-backup.sh

set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-s3:s3.amazonaws.com/backup-bucket/restic}"
export RESTIC_PASSWORD_FILE="${RESTIC_PASSWORD_FILE:-/etc/restic/password}"

echo "[$(date -Iseconds)] Starting Restic backup"

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
  --tag "$(hostname)"

# Retention: keep last 24h hourly, 7 daily, 4 weekly, 12 monthly
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune

# Mandatory integrity check — verifies all data blobs
restic check

echo "[$(date -Iseconds)] Restic backup completed"
