#!/usr/bin/env bash
# purpose: fail CI/commit if Go standard layout drifts (cmd/, internal/, no external internal imports).
# consumes: repo root cwd; expects go.mod present.
# produces: exit 0 on pass, non-zero with reason on fail.
# depends-on: bash, grep, find — no external tools.
# token-budget-impact: 0 — shell script, not loaded into LLM context.
set -euo pipefail

required=("cmd" "internal/handler" "internal/service" "internal/repository" "internal/model")
for d in "${required[@]}"; do
  [[ -d "$d" ]] || { echo "MISSING required dir: $d"; exit 1; }
done

# Verify internal/ is not imported from outside this module.
mod=$(go list -m)
if grep -RIn "\"$mod/internal/" --include="*.go" -- . | grep -v "^./$mod" >/dev/null 2>&1; then
  echo "FAIL — internal/ package imported from outside module"
  exit 1
fi

go vet ./...
echo "layout ok"
