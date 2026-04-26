#!/usr/bin/env bash
# spec-quality-gate.sh — check completeness before moving to design phase
# Usage: spec-quality-gate.sh SPEC_FILE
# Returns non-zero if any required section is missing.

SPEC=${1:?Usage: spec-quality-gate.sh spec.md}
PASS=true

check() {
  local label=$1
  local pattern=$2
  if grep -qP "$pattern" "$SPEC" 2>/dev/null || grep -q "$pattern" "$SPEC" 2>/dev/null; then
    echo "PASS  $label"
  else
    echo "FAIL  $label"
    PASS=false
  fi
}

echo "Quality gate: $SPEC"
echo "---"

check "Problem Statement (Who)"       "Who:"
check "User Stories"                   "### US-"
check "Functional Requirements table"  "| FR-"
check "NFR table"                      "| NFR-"
check "Acceptance Criteria (Given)"    "Given:"
check "Out of Scope section"           "## Out of Scope"
check "Assumptions section"            "## Assumptions"
check "Dependencies section"           "## Dependencies"
check "Status field"                   "Status:"

echo "---"
if $PASS; then
  echo "Quality gate: PASS — ready for design phase"
else
  echo "Quality gate: FAIL — fix issues above before design"
  exit 1
fi
