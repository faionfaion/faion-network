#!/usr/bin/env bash
# scripts/check-layout.sh — fail commit if Go standard layout drifts.
# Run in CI and as a pre-commit hook.
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
