#!/bin/bash
# Scan a project for hardcoded hex colors outside design tokens
# Usage: bash audit-colors.sh src/
# Output: file:line → hardcoded value (to fix: replace with design token)

DIR="${1:-src}"

if ! command -v rg &> /dev/null; then
  echo "Error: ripgrep (rg) not installed. Run: apt install ripgrep"
  exit 1
fi

echo "Scanning $DIR for hardcoded hex colors..."
echo "---"

rg --type-add 'web:*.{tsx,ts,css,scss,jsx,js}' \
  --type web \
  -n '#[0-9a-fA-F]{3,6}\b' "$DIR" \
  | grep -v '\.tokens\.' \
  | grep -v 'colors\.ts' \
  | grep -v '\.stories\.' \
  | awk -F: '{print $1 ":" $2 " → " $3}' \
  | head -100

echo "---"
echo "Fix: replace hardcoded values with design tokens from your token file."
echo "Common tokens: --color-primary, --color-danger, --color-success"
