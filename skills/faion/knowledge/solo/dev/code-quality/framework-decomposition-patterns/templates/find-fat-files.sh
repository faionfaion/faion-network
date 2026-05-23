#!/usr/bin/env bash
# purpose: top-20 longest Python app files (excludes tests/migrations).
# consumes: repo-path (default current dir).
# produces: stdout LoC + path of fat candidates.
# depends-on: git, wc, sort.
# token-budget-impact: ~50 tokens (helper only).

# find-fat-files.sh — top-20 longest Python app files (excludes tests/migrations)
# Usage: ./find-fat-files.sh [repo-path]
cd "${1:-.}"
git ls-files '*.py' | grep -Ev 'tests?/|migrations?/' \
  | xargs wc -l 2>/dev/null | sort -rn | head -20
