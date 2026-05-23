#!/usr/bin/env bash
# spec-trace-check.sh
#
# Verify every FR-X in spec.md references a US-X and has an AC entry.
#
# Usage:
#   bash spec-trace-check.sh spec.md
#
# Exit codes:
#   0 — all traces found
#   1 — missing traces detected

set -euo pipefail

SPEC="${1:?usage: spec-trace-check.sh spec.md}"

if [ ! -f "$SPEC" ]; then
    echo "ERROR: $SPEC not found" >&2
    exit 1
fi

FAILED=0

# Check every FR has a US reference in its row
echo "=== FR → US traceability ==="
FRS=$(grep -oP 'FR-\d+' "$SPEC" | sort -u)
for fr in $FRS; do
    # FR is in a table row — check the row contains a US-X reference
    if ! grep -P "\\|\s*$fr\s*\\|" "$SPEC" | grep -qP "US-\d+"; then
        echo "MISSING: $fr has no US-X reference in requirements table"
        FAILED=1
    fi
done

# Check every FR is referenced in at least one AC
echo "=== FR → AC traceability ==="
for fr in $FRS; do
    if ! grep -A 10 "^### AC-" "$SPEC" | grep -q "$fr"; then
        echo "WARNING: $fr has no AC entry referencing it"
    fi
done

# Check every US has "so that" benefit
echo "=== US benefit clause ==="
US_COUNT=$(grep -c "^### US-" "$SPEC" || echo 0)
SO_THAT_COUNT=$(grep -c "So that" "$SPEC" || echo 0)
if [ "$SO_THAT_COUNT" -lt "$US_COUNT" ]; then
    echo "WARNING: $US_COUNT user stories but only $SO_THAT_COUNT 'So that' clauses"
fi

if [ "$FAILED" -eq 0 ]; then
    echo "Trace check complete for $SPEC — all FRs have US references"
else
    echo "Trace check FAILED for $SPEC"
    exit 1
fi
