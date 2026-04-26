#!/usr/bin/env bash
# sync-patterns.sh — Report High-confidence patterns not yet in CLAUDE.md
# Usage: bash sync-patterns.sh .aidocs/memory/patterns.md CLAUDE.md

set -euo pipefail

PATTERNS="${1:-.aidocs/memory/patterns.md}"
CLAUDE="${2:-CLAUDE.md}"

if [[ ! -f "$PATTERNS" ]]; then
  echo "ERROR: patterns file not found: $PATTERNS"
  exit 1
fi

if [[ ! -f "$CLAUDE" ]]; then
  echo "ERROR: CLAUDE.md not found: $CLAUDE"
  exit 1
fi

echo "Checking for High-confidence patterns missing from CLAUDE.md..."
echo "Patterns file: $PATTERNS"
echo "CLAUDE.md: $CLAUDE"
echo "---"

MISSING=0

# Extract pattern names with High confidence
while IFS= read -r line; do
  if [[ "$line" =~ ^##[[:space:]](.+) ]]; then
    PATTERN_NAME="${BASH_REMATCH[1]}"
  fi
  if [[ "$line" =~ \*\*Confidence:\*\*[[:space:]]High ]]; then
    # Check if pattern name appears in CLAUDE.md
    if ! grep -qF "$PATTERN_NAME" "$CLAUDE"; then
      echo "NOT IN CLAUDE.md: $PATTERN_NAME"
      MISSING=$((MISSING + 1))
    else
      echo "OK: $PATTERN_NAME"
    fi
  fi
done < "$PATTERNS"

echo "---"
if [[ $MISSING -eq 0 ]]; then
  echo "All High-confidence patterns are referenced in CLAUDE.md"
  exit 0
else
  echo "$MISSING High-confidence pattern(s) need to be added to CLAUDE.md"
  echo "Use prompt-extract.txt CLAUDE.MD SYNC PROMPT to generate the additions"
  exit 1
fi
