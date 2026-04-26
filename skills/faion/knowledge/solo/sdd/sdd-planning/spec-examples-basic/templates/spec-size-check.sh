#!/usr/bin/env bash
# spec-size-check.sh — verify a spec file fits the condensed format thresholds
# Usage: spec-size-check.sh SPEC_FILE
# Returns non-zero if any threshold is exceeded.

SPEC=${1:?Usage: spec-size-check.sh spec.md}

FR_COUNT=$(grep -c "^| FR-" "$SPEC" 2>/dev/null || echo 0)
US_COUNT=$(grep -c "^### US-" "$SPEC" 2>/dev/null || echo 0)
AC_COUNT=$(grep -c "^### AC-" "$SPEC" 2>/dev/null || echo 0)
LINE_COUNT=$(wc -l < "$SPEC")

echo "Spec: $SPEC"
echo "US: $US_COUNT | FR: $FR_COUNT | AC: $AC_COUNT | Lines: $LINE_COUNT"

FAIL=false

if [ "$FR_COUNT" -gt 6 ]; then
  echo "WARN: $FR_COUNT FRs — condensed format allows max 6; consider full spec-structure"
  FAIL=true
fi

if [ "$US_COUNT" -gt 3 ]; then
  echo "WARN: $US_COUNT User Stories — condensed format allows max 3"
  FAIL=true
fi

if [ "$AC_COUNT" -lt 2 ]; then
  echo "WARN: Need at least 1 happy path + 1 error AC (found $AC_COUNT)"
  FAIL=true
fi

if [ "$LINE_COUNT" -gt 80 ]; then
  echo "WARN: $LINE_COUNT lines — condensed spec should be under 80 lines"
  FAIL=true
fi

if $FAIL; then
  echo "RESULT: WARN — review thresholds above"
  exit 1
else
  echo "RESULT: PASS — spec fits condensed format"
fi
