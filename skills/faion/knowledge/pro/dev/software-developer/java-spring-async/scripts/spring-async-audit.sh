#!/usr/bin/env bash
# spring-async-audit.sh — flag common @Async anti-patterns in a Spring Boot project.
# Usage: spring-async-audit.sh <project-root>
# Exit 1 if critical issues found (self-invocation, missing executor name, tx+async).
set -euo pipefail
root="${1:?usage: spring-async-audit.sh PROJECT_ROOT}"
fail=0
echo "# Spring @Async audit ($root)"

echo "## Self-invocation: this.<asyncMethod>() inside same @Service"
grep -rl '@Async' "$root/src/main" --include='*.java' 2>/dev/null | while read -r f; do
  for m in $(grep -E '@Async' "$f" -A 1 | grep -oE '[a-z][a-zA-Z0-9]+\(' | tr -d '('); do
    grep -nE "this\.${m}\(" "$f" | while read -r match; do
      echo "  $f: $match  [self-invocation]"; fail=1
    done
  done
done || true

echo "## @Async without explicit executor name"
grep -rEn '@Async$|@Async\s*$|@Async\(\)' "$root/src/main" --include='*.java' 2>/dev/null \
  | tee /tmp/async.noexec || true
[[ -s /tmp/async.noexec ]] && fail=1

echo "## void-returning @Async (without AsyncUncaughtExceptionHandler)"
grep -rl '@Async' "$root/src/main" --include='*.java' 2>/dev/null \
  | xargs grep -l 'public\s\+void' 2>/dev/null \
  | xargs grep -rL 'AsyncUncaughtExceptionHandler' 2>/dev/null \
  | tee /tmp/async.exc || true

echo "## @Transactional + @Async on same method"
grep -rEn '@Async\b' "$root/src/main" --include='*.java' -B 2 2>/dev/null \
  | grep '@Transactional' | tee /tmp/async.tx || true
[[ -s /tmp/async.tx ]] && fail=1

echo "## Executor missing setWaitForTasksToCompleteOnShutdown"
grep -rEl 'new ThreadPoolTaskExecutor' "$root/src/main" --include='*.java' 2>/dev/null \
  | xargs grep -L 'setWaitForTasksToCompleteOnShutdown' 2>/dev/null \
  | tee /tmp/async.shutdown || true

echo "## Thread.sleep in tests (use Awaitility)"
grep -rEn 'Thread\.sleep\(' "$root/src/test" --include='*.java' 2>/dev/null \
  | tee /tmp/async.sleep || true

exit "$fail"
