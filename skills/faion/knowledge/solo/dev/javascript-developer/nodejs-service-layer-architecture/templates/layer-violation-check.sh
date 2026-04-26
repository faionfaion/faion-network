#!/bin/bash
# layer-violation-check.sh — Detect layer boundary violations in Node.js service layer.
# Run from project root. Reports Prisma in services, direct DB in controllers,
# and HTTP response calls in services.
set -euo pipefail

ERRORS=0

echo "=== Prisma in services (should be in repositories only) ==="
if grep -rn "PrismaClient\|prisma\." src/services/ 2>/dev/null; then
    ERRORS=$((ERRORS + 1))
else
    echo "None found"
fi

echo ""
echo "=== Direct DB calls in controllers ==="
if grep -rn "prisma\.\|findUnique\|findMany\|\.create(\|\.update(\|\.delete(" src/controllers/ 2>/dev/null; then
    ERRORS=$((ERRORS + 1))
else
    echo "None found"
fi

echo ""
echo "=== HTTP response calls in services (res.status/res.json) ==="
if grep -rn "res\.status\|res\.json\|res\.send" src/services/ 2>/dev/null; then
    ERRORS=$((ERRORS + 1))
else
    echo "None found"
fi

echo ""
echo "=== process.env outside config/ ==="
if grep -rn "process\.env\." src/ --include="*.ts" \
    --exclude-dir=config 2>/dev/null; then
    ERRORS=$((ERRORS + 1))
else
    echo "None found"
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "FAIL: $ERRORS layer violation category(ies) found"
    exit 1
else
    echo "OK: No layer violations detected"
fi
