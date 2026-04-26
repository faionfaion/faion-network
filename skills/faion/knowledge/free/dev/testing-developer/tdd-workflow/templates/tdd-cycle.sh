#!/usr/bin/env bash
# tdd-cycle.sh — guided TDD cycle for a single behavior
#
# Usage:
#   ./tdd-cycle.sh "test_command" "impl_file"
#
# Example:
#   ./tdd-cycle.sh "pytest tests/test_cart.py::test_discount -x" "src/cart.py"
#
# The script walks you through RED → GREEN → REFACTOR with confirmation prompts.

set -euo pipefail

TEST_CMD="${1:-pytest -x --tb=short}"
IMPL_FILE="${2:-}"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

confirm() {
    local msg="$1"
    echo -e "${YELLOW}${msg}${RESET}"
    read -rp "Press Enter when ready... " _
}

echo "=============================="
echo "  TDD Cycle"
echo "=============================="
echo ""

# ---- RED ----
echo -e "${RED}[RED] Write a failing test for ONE behavior.${RESET}"
echo "     Test file should NOT pass yet — implementation does not exist."
echo ""
confirm "When done writing the test, press Enter to run it."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${RED}WARNING: Test PASSED without implementation.${RESET}"
    echo "This means the test is testing nothing, or the behavior already exists."
    echo "Review your test before proceeding."
    exit 1
else
    echo ""
    echo -e "${GREEN}Good — test is FAILING as expected (RED).${RESET}"
fi

echo ""

# ---- GREEN ----
echo -e "${GREEN}[GREEN] Write minimal implementation to make the test pass.${RESET}"
if [[ -n "$IMPL_FILE" ]]; then
    echo "     Edit: $IMPL_FILE"
fi
echo "     Do NOT add features beyond what the failing test requires."
echo ""
confirm "When done writing implementation, press Enter to run tests."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${GREEN}All tests PASS (GREEN).${RESET}"
else
    echo ""
    echo -e "${RED}Tests still FAILING.${RESET}"
    echo "Fix the implementation until all tests pass, then re-run this script."
    exit 1
fi

echo ""

# ---- REFACTOR ----
echo -e "${YELLOW}[REFACTOR] Improve code quality without changing behavior.${RESET}"
echo "     - Extract functions, rename variables, remove duplication"
echo "     - Do NOT add new behavior here — start a new RED cycle for that"
echo ""
confirm "When done refactoring (or if no refactor needed), press Enter to verify."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${GREEN}All tests PASS after refactor.${RESET}"
    echo ""
    echo "=============================="
    echo -e "${GREEN}TDD cycle complete.${RESET}"
    echo "Commit test + implementation together, then start next RED cycle."
    echo "=============================="
else
    echo ""
    echo -e "${RED}Tests broke during refactor.${RESET}"
    echo "Revert refactor changes until tests pass again."
    exit 1
fi
