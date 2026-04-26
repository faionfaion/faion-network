#!/usr/bin/env bash
# tdd.sh — single-behavior RED-GREEN-REFACTOR loop driver.
# Usage: ./tdd.sh path/to/test_file.py::test_name
# For agents: replace read prompts with explicit subagent invocations.
set -e
TEST="${1:?usage: tdd.sh path/to/test::test_name}"
echo "=== RED: expecting 1 failed, 0 passed ==="
pytest "$TEST" -x && { echo "Expected FAIL but got PASS — check test isolation"; exit 1; }
read -rp "Write minimal implementation, then press ENTER for GREEN... "
echo "=== GREEN: expecting 1 passed ==="
pytest "$TEST" -x
read -rp "Refactor code (no new features), then press ENTER for full suite... "
echo "=== REFACTOR: running full suite ==="
pytest -q
