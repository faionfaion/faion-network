#!/usr/bin/env bash
# query-budget.sh — fail CI if any feature test exceeds N queries.
# Usage: query-budget.sh BUDGET (default 15)
# Requires: DB_LOG_QUERIES=true support in the test suite.
set -euo pipefail
BUDGET="${1:-15}"
LOG=$(mktemp)
DB_LOG_QUERIES=true php artisan test --log-junit "$LOG" --testdox 2>&1 | tee /tmp/test.out
python3 - "$BUDGET" <<'PY'
import re, sys
budget = int(sys.argv[1])
text = open("/tmp/test.out").read()
fails = []
for m in re.finditer(r"^\s*[\w\\:]+.*?queries:\s*(\d+)", text, re.M):
    n = int(m.group(1))
    if n > budget:
        fails.append((m.group(0).strip(), n))
if fails:
    print(f"\nQuery budget {budget} exceeded:")
    for name, q in fails:
        print(f"  {name}: {q} queries")
    sys.exit(1)
print(f"OK: all tests within {budget} queries")
PY
