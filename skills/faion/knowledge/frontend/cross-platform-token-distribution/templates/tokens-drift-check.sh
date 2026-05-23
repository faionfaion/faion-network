#!/usr/bin/env bash
# tokens-drift-check.sh — fail CI if platform outputs diverge from source
# Usage: bash tokens-drift-check.sh
# Requires: style-dictionary installed, config at tokens/config.json
set -euo pipefail

git stash --include-untracked --quiet || true
npx style-dictionary build --config tokens/config.json

if ! git diff --quiet -- 'platforms/'; then
  echo "FAIL: token outputs are stale. Run 'npm run tokens:build' and commit."
  git diff --stat -- 'platforms/'
  exit 1
fi

git stash pop --quiet 2>/dev/null || true
echo "OK: token outputs in sync."
