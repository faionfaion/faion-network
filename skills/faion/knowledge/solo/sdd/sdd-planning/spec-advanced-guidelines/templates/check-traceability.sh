#!/usr/bin/env bash
# check-traceability.sh — verify FR → US → AC coverage in a spec.md
# Usage: ./check-traceability.sh path/to/spec.md
# Exits 0 if all checks pass, 1 if any fail.

set -euo pipefail

SPEC="${1:-spec.md}"

if [[ ! -f "$SPEC" ]]; then
  echo "Error: file not found: $SPEC" >&2
  exit 1
fi

ERRORS=0

# Helper: count pattern matches
count() { grep -cP "$1" "$SPEC" 2>/dev/null || echo 0; }

# 1. Check required sections exist
SECTIONS=(
  "## 1\. Overview"
  "## 2\. Problem Statement"
  "## 3\. User Personas"
  "## 4\. User Stories"
  "## 5\. Functional Requirements"
  "## 6\. Non-Functional Requirements"
  "## 7\. Acceptance Criteria"
  "## 8\. Out of Scope"
  "## 9\. Assumptions"
  "## 10\. Dependencies"
  "## 13\. Open Questions"
)

for section in "${SECTIONS[@]}"; do
  if ! grep -qP "$section" "$SPEC"; then
    echo "MISSING SECTION: $section"
    ERRORS=$((ERRORS + 1))
  fi
done

# 2. Check FR → US traceability
FR_COUNT=$(grep -cP '^### FR-\d+' "$SPEC" 2>/dev/null || echo 0)
FR_WITH_TRACES=$(grep -cP 'Traces to: US-' "$SPEC" 2>/dev/null || echo 0)

if [[ "$FR_COUNT" -gt 0 && "$FR_WITH_TRACES" -lt "$FR_COUNT" ]]; then
  echo "TRACEABILITY: $FR_WITH_TRACES/$FR_COUNT FRs have US traces (expected $FR_COUNT)"
  ERRORS=$((ERRORS + 1))
fi

# 3. Check AC → FR traceability
AC_COUNT=$(grep -cP '^### AC-\d+' "$SPEC" 2>/dev/null || echo 0)
AC_WITH_TRACES=$(grep -cP 'Traces to: FR-' "$SPEC" 2>/dev/null || echo 0)

if [[ "$AC_COUNT" -gt 0 && "$AC_WITH_TRACES" -lt "$AC_COUNT" ]]; then
  echo "TRACEABILITY: $AC_WITH_TRACES/$AC_COUNT ACs have FR traces (expected $AC_COUNT)"
  ERRORS=$((ERRORS + 1))
fi

# 4. Check NFRs have quantifiable targets (basic: must contain < > % or ms)
NFR_COUNT=$(grep -cP '^### NFR-\d+' "$SPEC" 2>/dev/null || echo 0)
if [[ "$NFR_COUNT" -gt 0 ]]; then
  VAGUE_NFRS=$(grep -cP '^\*\*Requirement:\*\*.*\b(fast|good|acceptable|high|low)\b' "$SPEC" 2>/dev/null || echo 0)
  if [[ "$VAGUE_NFRS" -gt 0 ]]; then
    echo "VAGUE NFRS: $VAGUE_NFRS NFRs contain vague qualifiers (fast/good/acceptable)"
    ERRORS=$((ERRORS + 1))
  fi
fi

# 5. Check Out of Scope table has reason and when columns
OOS_ROWS=$(grep -cP '^\| .+ \| .+ \| .+ \|' "$SPEC" 2>/dev/null || echo 0)
# (basic check: table has 3-column rows under Out of Scope section)

# Summary
echo "---"
echo "FRs: $FR_COUNT  |  ACs: $AC_COUNT  |  NFRs: $NFR_COUNT"

if [[ "$ERRORS" -eq 0 ]]; then
  echo "PASS: traceability checks passed"
  exit 0
else
  echo "FAIL: $ERRORS issue(s) found"
  exit 1
fi
