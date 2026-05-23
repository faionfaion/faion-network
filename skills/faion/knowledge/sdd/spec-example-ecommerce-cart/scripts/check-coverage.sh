#!/usr/bin/env bash
# check-coverage.sh — Print all unchecked AC coverage items from a spec file.
# Usage: ./check-coverage.sh spec.md
# Output: line number and unchecked item text (potential coverage gaps)
set -euo pipefail

SPEC="${1:?Usage: $0 spec.md}"

echo "=== Unchecked AC coverage items in: $SPEC ==="
grep -n '- \[ \]' "$SPEC" | sed 's/- \[ \]/UNCHECKED:/' || echo "(none found)"
echo ""
echo "=== Count ==="
count=$(grep -c '- \[ \]' "$SPEC" 2>/dev/null || echo 0)
echo "$count unchecked items"
