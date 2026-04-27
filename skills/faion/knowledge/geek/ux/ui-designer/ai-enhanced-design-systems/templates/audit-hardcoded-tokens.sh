#!/usr/bin/env bash
# audit-hardcoded-tokens.sh — Find hardcoded design values that should use CSS custom properties.
# Usage: ./audit-hardcoded-tokens.sh (run from repo root)
# Output: hex colors and px spacing values not using var(--token) pattern
set -euo pipefail

echo "=== Hardcoded Hex Colors ==="
grep -rn --include="*.css" --include="*.scss" --include="*.tsx" --include="*.ts" \
  -E '#[0-9a-fA-F]{3,8}(?![0-9a-fA-F])' \
  --exclude-dir=node_modules \
  . | grep -v 'var(--' | head -50

echo ""
echo "=== Hardcoded Spacing (px not in token pattern) ==="
grep -rn --include="*.css" --include="*.scss" \
  -E '[^-]([0-9]{2,3}px)' \
  --exclude-dir=node_modules \
  . | grep -v 'var(--\|1px\|2px\|border' | head -50
