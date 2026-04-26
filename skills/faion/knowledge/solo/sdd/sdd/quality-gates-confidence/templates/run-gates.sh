#!/usr/bin/env bash
# run-gates.sh — Run quality gates for a feature task
# Usage: bash run-gates.sh [--gate L1] [--all] [--report path]
#
# By default runs L1-L5 (automated gates only).
# L6 (human review) is always manual — this script skips it.
#
# Options:
#   --gate L1       Run only the specified gate
#   --all           Run all gates including L6 (marks L6 as MANUAL)
#   --report PATH   Write report to this file (default: gate-report.md)
#   --threshold N   Confidence threshold (default: 90)

set -euo pipefail

GATE=""
RUN_ALL=false
REPORT="gate-report.md"
THRESHOLD=90
FEATURE_NAME="${FEATURE:-unknown}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gate)     GATE="$2"; shift 2 ;;
    --all)      RUN_ALL=true; shift ;;
    --report)   REPORT="$2"; shift 2 ;;
    --threshold) THRESHOLD="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

PASS=0
FAIL=0
SKIP=0

run_check() {
  local gate="$1"
  local name="$2"
  local cmd="$3"
  echo "  Running: $cmd"
  if eval "$cmd" > /tmp/gate-output 2>&1; then
    echo "  PASS: $name"
    PASS=$((PASS + 1))
    return 0
  else
    echo "  FAIL: $name"
    echo "  Output: $(head -5 /tmp/gate-output)"
    FAIL=$((FAIL + 1))
    return 1
  fi
}

run_gate_L1() {
  echo "=== L1: Syntax & Format ==="
  run_check L1 "ruff lint" "ruff check . --select E,F,I --quiet" || true
  run_check L1 "ruff format" "ruff format --check . --quiet" || true
}

run_gate_L2() {
  echo "=== L2: Unit Tests ==="
  run_check L2 "pytest unit" "pytest tests/unit/ -x --tb=short -q" || true
}

run_gate_L3() {
  echo "=== L3: Integration Tests ==="
  if [[ -d "tests/integration" ]]; then
    run_check L3 "pytest integration" "pytest tests/integration/ -x --tb=short -q" || true
  else
    echo "  SKIP: No integration tests directory"
    SKIP=$((SKIP + 1))
  fi
}

run_gate_L4() {
  echo "=== L4: Spec Compliance ==="
  if [[ -d "tests/acceptance" ]]; then
    run_check L4 "pytest acceptance" "pytest tests/acceptance/ -x --tb=short -q" || true
  else
    echo "  SKIP: No acceptance tests directory"
    SKIP=$((SKIP + 1))
  fi
}

run_gate_L5() {
  echo "=== L5: Non-Functional ==="
  if command -v bandit > /dev/null 2>&1; then
    run_check L5 "bandit security" "bandit -r . -l -q -x tests/" || true
  else
    echo "  SKIP: bandit not installed"
    SKIP=$((SKIP + 1))
  fi
}

# Run gates
if [[ -n "$GATE" ]]; then
  "run_gate_${GATE}"
elif [[ "$RUN_ALL" == true ]]; then
  run_gate_L1
  run_gate_L2
  run_gate_L3
  run_gate_L4
  run_gate_L5
  echo "=== L6: Human Review === (MANUAL — not automated)"
  SKIP=$((SKIP + 1))
else
  run_gate_L1
  run_gate_L2
  run_gate_L3
  run_gate_L4
  run_gate_L5
fi

TOTAL=$((PASS + FAIL + SKIP))
echo ""
echo "=== Summary ==="
echo "PASS: $PASS / FAIL: $FAIL / SKIP: $SKIP / TOTAL: $TOTAL"

if [[ $FAIL -gt 0 ]]; then
  echo "RESULT: FAIL — fix $FAIL failing check(s) before proceeding"
  exit 1
else
  echo "RESULT: PASS — all automated gates passed"
  exit 0
fi
