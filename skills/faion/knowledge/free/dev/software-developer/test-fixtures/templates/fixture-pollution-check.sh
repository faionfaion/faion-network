#!/usr/bin/env bash
# fixture-pollution-check.sh — detect order-dependent test failures.
# Runs pytest multiple times with random ordering seeds.
# Usage: fixture-pollution-check.sh [PYTEST_ARGS...]
# Example: fixture-pollution-check.sh tests/
set -euo pipefail
RUNS="${RUNS:-3}"
SEEDS=()
FAILED=false

for i in $(seq 1 "$RUNS"); do
  S=$RANDOM
  SEEDS+=("$S")
  echo "=== run $i seed=$S ==="
  if pytest -p randomly --randomly-seed="$S" -q "$@" >".pytest-pollution-$i.log" 2>&1; then
    echo "  OK"
  else
    echo "  FAIL"
    FAILED=true
    grep -E "FAILED|ERROR" ".pytest-pollution-$i.log" | head -20
  fi
done

if $FAILED; then
  echo ""
  echo "Order-dependent failures detected. Seeds: ${SEEDS[*]}"
  echo "Reproduce: pytest -p randomly --randomly-seed=<seed>"
  exit 1
fi
echo "OK — no order dependency in $RUNS runs"
