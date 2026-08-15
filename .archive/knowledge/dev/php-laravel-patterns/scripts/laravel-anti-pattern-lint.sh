#!/usr/bin/env bash
# laravel-anti-pattern-lint.sh — Detect Laravel layering antipatterns.
#
# Usage:
#   laravel-anti-pattern-lint.sh PROJECT_ROOT
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

echo "## Fat controller methods (>20 lines)"
for f in $(find "$root/app/Http/Controllers" -name '*.php' 2>/dev/null); do
  awk '/public function/,/^    \}/' "$f" | awk -v RS='}\n    ' 'length > 1500 { print FILENAME": fat method" }'
done

echo "## Inline validate() in controllers"
grep -rEn '\$request->validate\(' "$root/app/Http/Controllers" --include='*.php' 2>/dev/null && fail=1 || true

echo "## DB::transaction in controllers"
grep -rEn 'DB::transaction' "$root/app/Http/Controllers" --include='*.php' 2>/dev/null && fail=1 || true

echo "## Raw model returned (return \$var;)"
grep -rEn '^\s*return\s+\$[a-z][A-Za-z]*;' "$root/app/Http/Controllers" --include='*.php' 2>/dev/null && echo "  review needed" || true

echo "## abort(403) inline auth checks"
grep -rEn 'abort\(403' "$root/app/Http/Controllers" --include='*.php' 2>/dev/null && fail=1 || true

exit "$fail"
