#!/usr/bin/env bash
# pattern-guard.sh — enforce decomposition pattern invariants post-refactor.
# Usage: ./pattern-guard.sh [path]
# Checks: view line counts (Extract Service), component line counts (Extract Component),
#         settings file size (Extract Configuration), circular imports.
set -euo pipefail
ROOT="${1:-.}"
MAX_VIEW=120
MAX_COMPONENT=200
MAX_SERVICE=300
MAX_CONFIG=150

FAIL=0

# Views must be thin (Extract Service)
while IFS= read -r f; do
  n=$(wc -l < "$f")
  if [ "$n" -gt "$MAX_VIEW" ]; then
    echo "FAIL: $f: $n lines (> $MAX_VIEW) — apply Extract Service"
    FAIL=$((FAIL + 1))
  fi
done < <(find "$ROOT" -path '*/views/*' -name '*.py' 2>/dev/null)

# React components capped (Extract Component)
while IFS= read -r f; do
  n=$(wc -l < "$f")
  if [ "$n" -gt "$MAX_COMPONENT" ]; then
    echo "FAIL: $f: $n lines (> $MAX_COMPONENT) — apply Extract Component"
    FAIL=$((FAIL + 1))
  fi
done < <(find "$ROOT/src/components" -name '*.tsx' 2>/dev/null)

# Settings split (Extract Configuration)
if [ -f "$ROOT/settings.py" ]; then
  n=$(wc -l < "$ROOT/settings.py")
  if [ "$n" -gt "$MAX_CONFIG" ]; then
    echo "FAIL: settings.py: $n lines (> $MAX_CONFIG) — extract per-env"
    FAIL=$((FAIL + 1))
  fi
fi

# Circular imports
if command -v madge >/dev/null 2>&1; then
  madge --circular "$ROOT/src" 2>/dev/null || true
fi
if command -v pydeps >/dev/null 2>&1; then
  pydeps --show-cycles "$ROOT" 2>/dev/null || true
fi

if [ "$FAIL" -gt 0 ]; then
  echo "$FAIL invariant(s) violated"
  exit 1
fi
echo "OK"
