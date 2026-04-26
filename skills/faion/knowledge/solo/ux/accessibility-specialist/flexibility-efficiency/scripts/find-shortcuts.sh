#!/usr/bin/env bash
# find-shortcuts.sh — list all keyboard shortcut bindings in a JS/TS/JSX/TSX project
# Input: directory path (default: current directory)
# Output: sorted list of file:line matches for shortcut-related code
# Usage: bash find-shortcuts.sh src/

TARGET=${1:-.}
echo "=== Keyboard shortcut candidates in: $TARGET ==="
grep -rE "(Ctrl|Alt|Meta|Shift)\+[A-Za-z0-9]|key(down|up|press)|hotkey|shortcut|keybind" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  "$TARGET" \
  | grep -v "node_modules" \
  | grep -v ".test." \
  | awk -F: '{printf "%-60s %s\n", $1":"$2, $3}' \
  | sort -u
