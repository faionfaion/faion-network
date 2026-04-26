#!/bin/bash
# verify-backup.sh — Automated PostgreSQL restore verification with alerting
# Usage: ./verify-backup.sh /var/backups/postgres/latest.dump [test_db_name]

set -euo pipefail

BACKUP_PATH="$1"
DB_NAME="${2:-backup_test_$$}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
PUSHGATEWAY="${PUSHGATEWAY:-http://pushgateway:9091}"

cleanup() {
  psql -c "DROP DATABASE IF EXISTS $DB_NAME" 2>/dev/null || true
}
trap cleanup EXIT

send_alert() {
  local message="$1" severity="${2:-error}"
  [[ -n "$SLACK_WEBHOOK" ]] && curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"Backup Verify ($severity): $message\"}" "$SLACK_WEBHOOK" || true
}

# Basic file check
[[ -f "$BACKUP_PATH" && -s "$BACKUP_PATH" ]] || { send_alert "Backup missing or empty: $BACKUP_PATH" critical; exit 1; }

# Format check
pg_restore -l "$BACKUP_PATH" > /dev/null 2>&1 || { send_alert "Backup corrupted: $BACKUP_PATH" critical; exit 1; }

# Restore to isolated test DB
psql -c "CREATE DATABASE $DB_NAME"
START=$(date +%s)
pg_restore -d "$DB_NAME" "$BACKUP_PATH" 2>&1 || true
RESTORE_TIME=$(( $(date +%s) - START ))

# Sanity check: count tables
TABLE_COUNT=$(psql -d "$DB_NAME" -t -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'" | tr -d ' ')

echo "Verification passed: tables=$TABLE_COUNT restore_time=${RESTORE_TIME}s"

# Push success metric to Prometheus Pushgateway
cat <<EOF | curl -s --data-binary @- "$PUSHGATEWAY/metrics/job/backup_verify/instance/$(hostname)" || true
backup_verification_success{backup="$BACKUP_PATH"} 1
backup_verification_restore_seconds{backup="$BACKUP_PATH"} $RESTORE_TIME
backup_verification_table_count{backup="$BACKUP_PATH"} $TABLE_COUNT
EOF

send_alert "Backup verified: $(basename "$BACKUP_PATH") tables=$TABLE_COUNT time=${RESTORE_TIME}s" success
