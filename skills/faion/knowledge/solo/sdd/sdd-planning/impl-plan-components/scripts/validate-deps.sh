#!/usr/bin/env bash
# validate-deps.sh — Topological sort validator for task dependency list.
# Usage: echo "TASK-003 TASK-001\nTASK-003 TASK-002\nTASK-004 TASK-003" | ./validate-deps.sh
# Or:   ./validate-deps.sh < deps.txt
# Input: tab or space separated TASK DEPENDS_ON pairs, one per line
# Output: sorted execution order, or "CYCLE DETECTED" on circular dependency
# Requires: tsort (GNU coreutils)
set -euo pipefail

result=$(tsort 2>&1)
exit_code=$?

if echo "$result" | grep -q "loop\|cycle"; then
  echo "CYCLE DETECTED — fix circular dependencies before proceeding"
  echo "$result"
  exit 1
else
  echo "OK: valid DAG — execution order:"
  echo "$result"
  exit 0
fi
