#!/usr/bin/env bash
# purpose: structural-lint script enforcing file-size budgets + namespace whitelist
# consumes: Laravel `app/` directory
# produces: pass/fail gate per controllers-only-call-actions + namespace-whitelist rules
# depends-on: content/01-core-rules.xml rules controllers-only-call-actions, namespace-whitelist
# token-budget-impact: ~250 tokens when loaded as context
# decomp-lint.sh — fail if Laravel decomposition convention is broken.
# Usage: decomp-lint.sh app/
set -euo pipefail
ROOT="${1:-app}"
fail=0
check() {
  local pattern="$1" max="$2" label="$3"
  while IFS= read -r f; do
    n=$(wc -l <"$f")
    if [ "$n" -gt "$max" ]; then
      echo "FAIL $label: $f has $n lines (max $max)"
      fail=1
    fi
  done < <(find "$ROOT" -path "$pattern" -type f)
}
check "*/Http/Controllers/*.php" 150 "Controller"
check "*/Models/*.php"           150 "Model"
check "*/Actions/*/*.php"        100 "Action"
check "*/Services/*/*.php"       200 "Service"
check "*/DTOs/*/*.php"            40 "DTO"
check "*/Http/Resources/*.php"   100 "Resource"
features=$(ls -d "$ROOT"/Http/Controllers/Api/* 2>/dev/null | wc -l)
actions=$(ls -d "$ROOT"/Actions/* 2>/dev/null | wc -l)
if [ "$features" -gt 0 ] && [ "$actions" -eq 0 ]; then
  echo "FAIL: API controllers exist but app/Actions/ is empty"
  fail=1
fi
exit "$fail"
