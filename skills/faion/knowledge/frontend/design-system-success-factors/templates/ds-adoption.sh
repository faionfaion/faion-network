#!/usr/bin/env bash
# ds-adoption.sh — rough design-system component adoption proxy
# Usage: ./ds-adoption.sh [repo_root]
# Counts design-system component usage vs raw HTML elements in React TSX files
set -euo pipefail

ROOT="${1:-./apps}"

SYS=$(grep -RInE '<(Button|Input|Select|Card|Modal|Badge|Alert|Tooltip|Checkbox|Radio)\b' \
  "$ROOT" --include='*.tsx' | wc -l)

RAW=$(grep -RInE '<(button|input|select)[^>]*>' \
  "$ROOT" --include='*.tsx' | wc -l)

TOTAL=$((SYS + RAW))

if [[ $TOTAL -eq 0 ]]; then
  echo "No TSX files found under $ROOT"
  exit 0
fi

PCT=$(awk "BEGIN {printf \"%.1f\", ($SYS/$TOTAL)*100}")
echo "design-system:  $SYS"
echo "raw-html:       $RAW"
echo "total:          $TOTAL"
echo "ds-coverage:    ${PCT}%"
echo ""
echo "Note: split greenfield vs legacy dirs for accurate trend tracking."
echo "Note: this counts element names, not import graphs — wrap components may be missed."
