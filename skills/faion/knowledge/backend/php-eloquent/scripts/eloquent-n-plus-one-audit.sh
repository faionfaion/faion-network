#!/usr/bin/env bash
# eloquent-n-plus-one-audit.sh — Heuristic scan for likely N+1 sites in Laravel code.
#
# Usage:
#   eloquent-n-plus-one-audit.sh PROJECT_ROOT
#
# Exit codes:
#   0 = no obvious smells
#   1 = potential N+1 sites found (review required)
#   2 = usage error
set -euo pipefail

if [[ "${1:-}" == "--help" || $# -lt 1 ]]; then
  grep -E '^#' "$0" | sed 's/^# \{0,1\}//'
  [[ "${1:-}" == "--help" ]] && exit 0 || exit 2
fi

root="$1"
fail=0
echo "# Eloquent N+1 audit ($root)"

echo "## Model::all() inside foreach without ->with(...)"
grep -rEn '::all\(\)' "$root/app" --include='*.php' 2>/dev/null && fail=1 || true

echo "## foreach without preceding ->with() / ->load()"
grep -rEn 'foreach\s*\(\s*\$[a-zA-Z_]+' "$root/app" --include='*.php' -B 5 2>/dev/null \
  | grep -B 1 'foreach' | grep -E '->get\(\)|::all\(\)' && fail=1 || true

exit "$fail"
