#!/usr/bin/env bash
# spring-boot-layering-audit.sh — Lint Spring Boot layering antipatterns.
#
# Usage:
#   spring-boot-layering-audit.sh PROJECT_ROOT
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
echo "# Spring Boot layering audit ($root)"

echo "## @Transactional on controllers"
for f in $(grep -rl '@RestController\|@Controller' "$root/src/main" --include='*.java' 2>/dev/null); do
  grep -n '@Transactional' "$f" && { echo "  $f: @Transactional on controller"; fail=1; }
done

echo "## Field injection (@Autowired on fields)"
grep -rEn '^\s+@Autowired' "$root/src/main" --include='*.java' 2>/dev/null && fail=1 || true

echo "## Entities directly returned from controllers"
for f in $(grep -rl '@RestController\|@Controller' "$root/src/main" --include='*.java' 2>/dev/null); do
  grep -nE '(public|protected)\s+@?Entity' "$f" 2>/dev/null && { echo "  $f: entity exposed via controller"; fail=1; }
done

exit "$fail"
