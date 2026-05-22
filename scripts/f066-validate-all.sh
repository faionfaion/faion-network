#!/usr/bin/env bash
# F-066 Phase D: corpus-wide validation runner.
# Runs all 6 validators across knowledge tree, summarizes pass/fail per validator.

set -uo pipefail
cd "$(dirname "$0")/.."

REPORT="${1:-/tmp/f066-validate-report.txt}"
: > "$REPORT"

run() {
  local name="$1"; shift
  echo "=== $name ===" | tee -a "$REPORT"
  "$@" 2>&1 | tail -3 | tee -a "$REPORT"
  echo "" | tee -a "$REPORT"
}

run "1. validate-domains-index"             python3 scripts/validate-domains-index.py
run "2. validate-domain-index (all)"        python3 scripts/validate-domain-index.py --all
run "3. validate-methodology-v2 (all)"      bash -c 'fail=0; tot=0; for d in $(find skills/faion/knowledge -name AGENTS.md | xargs -I{} dirname {}); do tot=$((tot+1)); python3 scripts/validate-methodology-v2.py "$d" >/dev/null 2>&1 || fail=$((fail+1)); done; echo "summary: $((tot-fail))/$tot pass, $fail fail"'
run "4. validate-methodology-decision-tree" python3 scripts/validate-methodology-decision-tree.py --all
run "5. validate-methodology-templates"     python3 scripts/validate-methodology-templates.py --all
run "6. validate-methodology-scripts"       python3 scripts/validate-methodology-scripts.py --all

echo "report: $REPORT"
