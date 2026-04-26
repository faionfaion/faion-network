#!/usr/bin/env bash
# pytest-runner.sh — fast feedback loop for unit tests.
# Usage: pytest-runner.sh [test-scope]
# Runs only tests not marked integration/e2e/slow, deduplicates with no cache,
# stops on first failure, reports slowest 10.
set -euo pipefail
SCOPE="${1:-tests/}"
pytest "$SCOPE" \
  -x \
  --tb=short \
  -p no:cacheprovider \
  -m "not integration and not e2e and not slow" \
  --maxfail=1 \
  --randomly-seed=last \
  --durations=10
