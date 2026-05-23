#!/usr/bin/env bash
# adr-status.sh — list all ADRs with their current status
# Usage: adr-status.sh [ADR_DIR]
# Default ADR_DIR: docs/adr

ADR_DIR="${1:-docs/adr}"

if [ ! -d "$ADR_DIR" ]; then
  echo "ERROR: $ADR_DIR not found"
  exit 1
fi

echo "ADR | Title | Status"
echo "----|-------|-------"

for f in "$ADR_DIR"/*.md; do
  [ -f "$f" ] || continue
  num=$(basename "$f" .md | cut -d- -f1)
  title=$(head -1 "$f" | sed 's/^# //')
  status=$(grep -m1 "Status:" "$f" | sed 's/.*Status:[[:space:]]*//' | sed 's/\*//g' | tr -d '\n')
  echo "$num | $title | ${status:-unknown}"
done
