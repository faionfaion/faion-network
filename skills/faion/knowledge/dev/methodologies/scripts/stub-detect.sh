#!/usr/bin/env bash
# purpose: list sibling methodologies whose AGENTS.md is too thin (likely stub).
# consumes: parent skill directory passed as $1.
# produces: stdout list of short AGENTS.md paths (likely stubs).
# depends-on: bash, find, wc — stdlib only.
# token-budget-impact: 0 — shell script.
# stub-detect.sh — list sibling methodologies whose README is too thin.
# Usage: stub-detect.sh skills/faion/knowledge/free/dev/software-developer
set -euo pipefail
root="${1:?usage: stub-detect.sh PATH}"
threshold=80   # lines
echo "Methodology stubs (README <${threshold} lines):"
for d in "$root"/*/; do
  name=$(basename "$d")
  [ "$name" = "methodologies" ] && continue
  readme="$d/README.md"
  [ -f "$readme" ] || { echo "  $name (no README)"; continue; }
  lines=$(wc -l < "$readme")
  if [ "$lines" -lt "$threshold" ]; then
    has_ai="-"
    [ -f "$d/agent-integration.md" ] && has_ai="ai+"
    printf "  %-40s %4d lines  %s\n" "$name" "$lines" "$has_ai"
  fi
done
