#!/usr/bin/env bash
# validate-design.sh — Validate a design.md file for completeness
# Usage: bash validate-design.sh .aidocs/todo/feature-NNN-name/design.md [spec.md]

set -euo pipefail

DESIGN="${1:-}"
SPEC="${2:-}"

if [[ -z "$DESIGN" ]]; then
  echo "Usage: $0 <path-to-design.md> [path-to-spec.md]"
  exit 1
fi

if [[ ! -f "$DESIGN" ]]; then
  echo "ERROR: File not found: $DESIGN"
  exit 1
fi

ERRORS=0
WARNINGS=0

check() {
  local label="$1"
  local pattern="$2"
  local file="${3:-$DESIGN}"
  if ! grep -qE "$pattern" "$file"; then
    echo "MISSING: $label (pattern: $pattern)"
    ERRORS=$((ERRORS + 1))
  else
    echo "OK:      $label"
  fi
}

warn() {
  local label="$1"
  local pattern="$2"
  local file="${3:-$DESIGN}"
  if ! grep -qE "$pattern" "$file"; then
    echo "WARN:    $label (pattern: $pattern)"
    WARNINGS=$((WARNINGS + 1))
  else
    echo "OK:      $label"
  fi
}

echo "Checking: $DESIGN"
echo "---"

check "Overview section"           "## Overview"
check "Architecture section"       "## Architecture"
check "At least one AD-X"          "### AD-[0-9]"
check "AD Decision statement"      "^\*\*Decision:\*\*"
check "AD Rationale statement"     "^\*\*Rationale:\*\*"
check "AD Trade-offs statement"    "^\*\*Trade-offs"
check "Out of Scope section"       "## Out of Scope"
warn  "Open Questions section"     "## Open Questions"
warn  "API Contracts section"      "## API Contracts"
warn  "Data Models section"        "## Data Models"

# Check AD count vs options considered
AD_COUNT=$(grep -cE "^### AD-[0-9]" "$DESIGN" || true)
OPTIONS_COUNT=$(grep -cE "### Option [A-Z]:" "$DESIGN" || true)

echo "---"
echo "ADs found: $AD_COUNT"
echo "Options blocks found: $OPTIONS_COUNT"

if [[ $AD_COUNT -gt 0 && $OPTIONS_COUNT -lt $((AD_COUNT * 2)) ]]; then
  echo "WARN: Each AD-X should have at least 2 options considered"
  WARNINGS=$((WARNINGS + 1))
fi

# Cross-check with spec if provided
if [[ -n "$SPEC" && -f "$SPEC" ]]; then
  echo "---"
  echo "Cross-checking with spec: $SPEC"
  FR_COUNT=$(grep -cE "^### FR-[0-9]" "$SPEC" || true)
  echo "FRs in spec: $FR_COUNT"
  # Basic check: design should reference each FR number
  for i in $(seq 1 "$FR_COUNT"); do
    if ! grep -qE "FR-${i}" "$DESIGN"; then
      echo "MISSING: No reference to FR-${i} from spec in design"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi

echo "---"
if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
  echo "PASS: Design is complete"
  exit 0
elif [[ $ERRORS -eq 0 ]]; then
  echo "PASS with warnings: $WARNINGS advisory issue(s)"
  exit 0
else
  echo "FAIL: $ERRORS blocking issue(s), $WARNINGS warning(s)"
  exit 1
fi
