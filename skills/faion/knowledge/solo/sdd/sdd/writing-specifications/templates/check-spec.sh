#!/usr/bin/env bash
# check-spec.sh — Validate a spec.md file for completeness
# Usage: bash check-spec.sh .aidocs/todo/feature-NNN-name/spec.md

set -euo pipefail

SPEC="${1:-}"
if [[ -z "$SPEC" ]]; then
  echo "Usage: $0 <path-to-spec.md>"
  exit 1
fi

if [[ ! -f "$SPEC" ]]; then
  echo "ERROR: File not found: $SPEC"
  exit 1
fi

ERRORS=0

check() {
  local label="$1"
  local pattern="$2"
  if ! grep -qE "$pattern" "$SPEC"; then
    echo "MISSING: $label (pattern: $pattern)"
    ERRORS=$((ERRORS + 1))
  else
    echo "OK:      $label"
  fi
}

echo "Checking: $SPEC"
echo "---"

check "Problem Statement"     "## Problem"
check "Goals section"         "## Goals"
check "Non-Goals section"     "## Non-Goals"
check "At least one FR-X"     "### FR-[0-9]"
check "Given-When-Then AC"    "(Given|When|Then):"
check "Out of Scope section"  "## Out of Scope"
check "Success Criteria"      "## Success Criteria"

# Check that each FR has a Given-When-Then
FR_COUNT=$(grep -cE "^### FR-[0-9]" "$SPEC" || true)
AC_COUNT=$(grep -cE "^\- (Given|When|Then):" "$SPEC" || true)

echo "---"
echo "FRs found: $FR_COUNT"
echo "AC lines found: $AC_COUNT (expect >= $((FR_COUNT * 3)))"

if [[ $AC_COUNT -lt $((FR_COUNT * 3)) ]]; then
  echo "WARNING: Some FRs may be missing Given-When-Then acceptance criteria"
  ERRORS=$((ERRORS + 1))
fi

echo "---"
if [[ $ERRORS -eq 0 ]]; then
  echo "PASS: Spec looks complete ($FR_COUNT FRs, $AC_COUNT AC lines)"
  exit 0
else
  echo "FAIL: $ERRORS issue(s) found"
  exit 1
fi
