#!/usr/bin/env bash
# spring-async-audit.sh — Flag common @Async anti-patterns in a Spring Boot project.
#
# Usage:
#   spring-async-audit.sh PROJECT_ROOT
#
# Exit codes:
#   0 = clean
#   1 = critical issues found (self-invocation, bare @Async, async+tx, missing shutdown drain)
#   2 = usage error
set -euo pipefail

if [[ "${1:-}" == "--help" || $# -lt 1 ]]; then
  grep -E '^#' "$0" | sed 's/^# \{0,1\}//'
  [[ "${1:-}" == "--help" ]] && exit 0 || exit 2
fi

root="$1"
fail=0
echo "# Spring @Async audit ($root)"

echo "## Self-invocation: this.<asyncMethod>() inside same @Service"
grep -rl '@Async' "$root/src/main" --include='*.java' 2>/dev/null | while read -r f; do
  for m in $(grep -E '@Async' "$f" -A 1 | grep -oE '[a-z][a-zA-Z0-9]+\(' | tr -d '('); do
    grep -nE "this\.${m}\(" "$f" 2>/dev/null && { echo "  ${f}: self-invocation of ${m}"; fail=1; }
  done
done

echo "## @Async without explicit executor name"
if grep -rEn '@Async$|@Async\s*$|@Async\(\)' "$root/src/main" --include='*.java' 2>/dev/null; then
  fail=1
fi

echo "## @Transactional + @Async on same method"
grep -rEn '@Async' "$root/src/main" --include='*.java' -B 2 2>/dev/null | grep '@Transactional' && fail=1 || true

echo "## ThreadPoolTaskExecutor missing setWaitForTasksToCompleteOnShutdown"
for f in $(grep -rEl 'new ThreadPoolTaskExecutor' "$root/src/main" --include='*.java' 2>/dev/null); do
  grep -q 'setWaitForTasksToCompleteOnShutdown' "$f" || { echo "  $f: missing shutdown drain"; fail=1; }
done

echo "## Thread.sleep in tests (use Awaitility)"
grep -rEn 'Thread\.sleep\(' "$root/src/test" --include='*.java' 2>/dev/null || true

exit "$fail"
