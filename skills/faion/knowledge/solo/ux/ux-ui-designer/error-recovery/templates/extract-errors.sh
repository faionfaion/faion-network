#!/usr/bin/env bash
# extract-errors.sh — extract error string candidates from Python/JS codebase
# Usage: bash extract-errors.sh ./src
# Output: file:line:match for each candidate error string
# Requires: ripgrep (rg)

TARGET=${1:-.}

echo "=== Python error strings ==="
rg --type py -n \
  '(raise|messages\.|error\s*=|detail\s*=)\s*["\x27]' \
  "$TARGET" | head -100

echo ""
echo "=== JavaScript/TypeScript error strings ==="
rg --type js --type ts -n \
  '(throw new Error|message:\s*["\x27]|errorMessage\s*=)' \
  "$TARGET" | head -100

echo ""
echo "=== Template error text ==="
rg -n 'Error|error|failed|invalid|not found|denied|unauthorized' \
  --glob '*.html' --glob '*.jsx' --glob '*.tsx' \
  "$TARGET" | grep -v '^\s*//' | head -100

echo ""
echo "Audit input written above. Review each string against the three-part framework:"
echo "  1. What happened (1=vague, 3=specific)"
echo "  2. Why it happened (1=missing, 3=contextual)"
echo "  3. How to fix it (1=no action, 3=specific actionable step)"
