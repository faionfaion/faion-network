#!/usr/bin/env bash
# F-066 Phase D: corpus-wide validation runner.
# Runs all 10 validators across the corpus, summarizes pass/fail per validator.

set -uo pipefail
cd "$(dirname "$0")/.."

# Fresh clone, first dev command: point git at the tracked hooks.
./scripts/install-hooks.sh --quiet 2>/dev/null || true

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
run "7. validate-lexicon"                   python3 scripts/validate-lexicon.py
run "8. validate-recipes"                   python3 scripts/validate-recipes.py
run "9. validate-fragments"                 python3 scripts/validate-fragments.py
run "10. validate-tools"                    python3 scripts/validate-tools.py
run "11. validate-vars-dictionary"          python3 scripts/validate-vars-dictionary.py
run "12. sync-crosslinks --check"           python3 scripts/sync-crosslinks-to-meta.py --check

echo "report: $REPORT"
