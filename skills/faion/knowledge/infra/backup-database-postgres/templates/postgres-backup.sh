#!/usr/bin/env bash
# purpose: PostgreSQL backup pipeline skeleton (dump + verify + S3 push + prune)
# consumes: PGHOST PGUSER PGDATABASE PGPASSWORD (from secrets manager); S3_BUCKET; RETENTION_DAYS
# produces: verified custom-format dump in S3 + local 7-day rolling copy
# depends-on: content/01-core-rules.xml (verify-before-upload, secret-hygiene, custom-format-required)
# token-budget-impact: ~250 tokens when loaded as context

set -euo pipefail

: "${PGHOST:?required}"
: "${PGUSER:?required}"
: "${PGDATABASE:?required}"
: "${PGPASSWORD:?required (pull from Vault / AWS Secrets Manager)}"
: "${S3_BUCKET:?required (e.g. s3://backups-prod/postgres/)}"

RETENTION_DAYS="${RETENTION_DAYS:-7}"
BACKUP_DIR="/var/backups/postgres"
TS=$(date -u +%Y%m%dT%H%M%SZ)
DUMP="$BACKUP_DIR/${PGDATABASE}_${TS}.dump"

mkdir -p "$BACKUP_DIR"

# 1. Custom-format dump
pg_dump -h "$PGHOST" -U "$PGUSER" -Fc "$PGDATABASE" > "$DUMP"

# 2. Verify BEFORE upload (rule: verify-before-upload)
if ! pg_restore -l "$DUMP" > /dev/null 2>&1; then
    echo "ERROR: backup file failed pg_restore -l integrity check" >&2
    exit 1
fi

# 3. Upload
aws s3 cp "$DUMP" "$S3_BUCKET/${PGDATABASE}/" --storage-class STANDARD_IA

# 4. Prune local
find "$BACKUP_DIR" -type f -name "*.dump" -mtime "+${RETENTION_DAYS}" -delete

echo "ok ${PGDATABASE} ${TS}"
