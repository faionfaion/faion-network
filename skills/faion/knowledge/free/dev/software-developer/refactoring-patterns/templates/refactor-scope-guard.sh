# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

#!/usr/bin/env bash
# scripts/refactor-scope-guard.sh — block sprawling refactor commits.
# Wire as pre-commit hook. Fails if a commit with "refactor:" title touches > 5 files.
set -euo pipefail

msg=$(git log -1 --format=%s 2>/dev/null || echo "")
[[ "$msg" =~ ^refactor: ]] || exit 0

files=$(git diff --cached --name-only | wc -l)
if (( files > 5 )); then
  echo "FAIL — refactor commit touches $files files (max 5). Split the change."
  exit 1
fi

echo "OK — refactor scope is within limits ($files files)"
