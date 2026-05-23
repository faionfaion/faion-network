#!/usr/bin/env bash
# help-audit.sh — check docs directory for broken internal links and stale content markers
# Input: docs directory path (default: docs/)
# Output: broken links and stale content markers
# Usage: bash help-audit.sh docs/

DOCS=${1:-docs}

echo "=== Broken internal links ==="
grep -rEo '\[.*?\]\(([^)]+)\)' "$DOCS" \
  | grep -v 'http' \
  | awk -F'(' '{print $2}' \
  | tr -d ')' \
  | while read -r link; do
      [ ! -f "$DOCS/$link" ] && echo "MISSING: $link"
    done

echo ""
echo "=== Potentially stale content (version markers, TODOs) ==="
grep -rn "TODO\|FIXME\|outdated\|deprecated\|v[0-9]\+\.[0-9]\+" \
  --include="*.md" "$DOCS" \
  | head -40
