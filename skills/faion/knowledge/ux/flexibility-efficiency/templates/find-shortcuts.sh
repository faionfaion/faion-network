#!/usr/bin/env bash
# find-shortcuts.sh — extract all keyboard shortcut registrations from a JS/TS codebase
# Usage: bash find-shortcuts.sh ./src
SRC="${1:-.}"

echo "=== onKeyDown handlers ==="
grep -r "onKeyDown\|onKeyUp\|addEventListener.*keydown" \
  --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
  "$SRC" \
  | grep -v node_modules \
  | grep -v ".test." \
  | sed 's/^/  /'

echo ""
echo "=== useHotkeys / hotkeys-js registrations ==="
grep -r "useHotkeys\|hotkeys(" \
  --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
  "$SRC" \
  | grep -v node_modules \
  | sed 's/^/  /'

echo ""
echo "=== Keyboard shortcut display (aria-keyshortcuts / kbd) ==="
grep -r "aria-keyshortcuts\|<kbd\|shortcut" \
  --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.html" \
  "$SRC" \
  | grep -v node_modules \
  | sed 's/^/  /'
