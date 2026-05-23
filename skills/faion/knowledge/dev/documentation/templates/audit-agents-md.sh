#!/usr/bin/env bash
# purpose: Sweep the repo and list directories missing CLAUDE.md / AGENTS.md.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Run periodically; add as a CI guard once baseline is clean.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
# audit-agents-md.sh — flag dirs where source files are newer than AGENTS.md by >14 days.
# Usage: bash audit-agents-md.sh [repo-root]
set -e
THRESH=$((14*24*60*60))
fail=0
while IFS= read -r dir; do
  agents="$dir/AGENTS.md"
  [ -f "$agents" ] || continue
  agents_ts=$(stat -c %Y "$agents")
  newest_src=$(find "$dir" -maxdepth 1 -type f \
      \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.go' \) \
      -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1)
  [ -z "$newest_src" ] && continue
  if [ $((newest_src - agents_ts)) -gt $THRESH ]; then
    echo "DRIFT: $agents (source newer by >14 days)"
    fail=1
  fi
done < <(find "${1:-.}" -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*')
exit $fail
