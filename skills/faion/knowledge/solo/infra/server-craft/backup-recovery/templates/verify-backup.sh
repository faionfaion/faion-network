#!/bin/bash
# verify-backup.sh
# Verify the latest backup is valid, complete, and recent.
#
# Exit codes: 0 = all OK, 1 = issues found

set -euo pipefail

BACKUP_BASE="/home/nero/backups"
LATEST=$(ls -td "$BACKUP_BASE"/20* 2>/dev/null | head -1 || true)

if [ -z "$LATEST" ]; then
    echo "FAIL: No backups found in $BACKUP_BASE"
    exit 1
fi

echo "=== Verifying backup: $LATEST ==="
ERRORS=0

# PostgreSQL dump
DUMP="$LATEST/database/nero_db.dump"
if [ -f "$DUMP" ]; then
    if pg_restore --list "$DUMP" > /dev/null 2>&1; then
        echo "OK   PostgreSQL dump: $(du -sh "$DUMP" | cut -f1)"
    else
        echo "FAIL PostgreSQL dump is corrupted"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "FAIL PostgreSQL dump missing: $DUMP"
    ERRORS=$((ERRORS + 1))
fi

# Redis RDB
RDB="$LATEST/redis/dump.rdb"
if [ -f "$RDB" ] && [ -s "$RDB" ]; then
    echo "OK   Redis dump: $(du -sh "$RDB" | cut -f1)"
else
    echo "FAIL Redis dump missing or empty"
    ERRORS=$((ERRORS + 1))
fi

# Critical config files
for cfg in ".env" "sshd_config"; do
    if [ -f "$LATEST/configs/$cfg" ]; then
        echo "OK   Config: $cfg"
    else
        echo "FAIL Config missing: $cfg"
        ERRORS=$((ERRORS + 1))
    fi
done

# Backup age (warn if older than 25h)
AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$LATEST")) / 3600 ))
if [ "$AGE_HOURS" -gt 25 ]; then
    echo "WARN Backup is ${AGE_HOURS}h old (expected < 25h)"
    ERRORS=$((ERRORS + 1))
else
    echo "OK   Backup age: ${AGE_HOURS}h"
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "RESULT: $ERRORS issues found"
    exit 1
else
    echo "RESULT: All checks passed"
    exit 0
fi
