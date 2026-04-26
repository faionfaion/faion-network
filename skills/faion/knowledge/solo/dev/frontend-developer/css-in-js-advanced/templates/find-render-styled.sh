#!/usr/bin/env bash
# find-render-styled.sh
# Flag styled.X definitions inside React component render bodies (perf footgun).
# Usage: bash find-render-styled.sh [src-dir]
set -euo pipefail
SRC="${1:-src}"

# Find component functions, then check for styled.X inside them
RESULT=$(grep -rEn "function [A-Z][a-zA-Z]*\s*\(" "$SRC" --include='*.tsx' -A 30 \
  | grep -E "(const|let) [A-Z][a-zA-Z]* = styled\." \
  || true)

if [ -n "$RESULT" ]; then
  echo "FAIL: styled components defined inside render bodies:"
  echo "$RESULT"
  exit 1
fi
echo "OK: no styled components defined inside render bodies"
