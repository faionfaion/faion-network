#!/usr/bin/env bash
# laravel-layering-audit.sh — Lint Laravel layering antipatterns.
#
# Usage:
#   laravel-layering-audit.sh PROJECT_ROOT
#
# Exit codes:
#   0 = clean
#   1 = violations found
#   2 = usage error
set -euo pipefail

if [[ "${1:-}" == "--help" || $# -lt 1 ]]; then
  grep -E '^#' "$0" | sed 's/^# \{0,1\}//'
  [[ "${1:-}" == "--help" ]] && exit 0 || exit 2
fi

root="$1"
fail=0
echo "# Laravel layering audit ($root)"

echo "## Eloquent calls in controllers"
for f in $(find "$root/app/Http/Controllers" -name '*.php' 2>/dev/null); do
  grep -nE '::(query|find|where|create|update|delete|all|first|firstOr)' "$f" 2>/dev/null && { echo "  $f: eloquent in controller"; fail=1; }
done

echo "## DB::transaction in controllers"
for f in $(find "$root/app/Http/Controllers" -name '*.php' 2>/dev/null); do
  grep -n 'DB::transaction' "$f" 2>/dev/null && { echo "  $f: tx in controller"; fail=1; }
done

echo "## Raw model returned from controller (return \$model;)"
for f in $(find "$root/app/Http/Controllers" -name '*.php' 2>/dev/null); do
  grep -nE 'return \$[a-z][A-Za-z]*;' "$f" 2>/dev/null && echo "  $f: possible raw model return — verify"
done

exit "$fail"
