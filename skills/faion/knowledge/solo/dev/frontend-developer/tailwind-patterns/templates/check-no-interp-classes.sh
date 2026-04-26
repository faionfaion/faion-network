#!/usr/bin/env bash
# check-no-interp-classes.sh
# Fail CI if dynamic Tailwind class interpolation is detected.
# JIT purges interpolated strings — they produce missing styles with no error.
#
# Bad:  className={`bg-${tone}-500`}
# Good: use lookup object with full literal class strings
#
# Add to .husky/pre-commit or GitHub Actions.
set -euo pipefail

SCAN_DIRS="${1:-src}"

echo "Scanning $SCAN_DIRS for dynamic Tailwind class interpolation..."

# Pattern: template literal inside className= or cva() containing a ${...} expression
MATCHES=$(git grep -nE \
  'className=\{?`[^`]*\$\{[^}]+\}[^`]*`|cva\([^)]*`[^`]*\$\{[^}]+\}[^`]*`' \
  -- "${SCAN_DIRS}/**/*.tsx" "${SCAN_DIRS}/**/*.ts" "${SCAN_DIRS}/**/*.jsx" 2>/dev/null || true)

if [[ -n "$MATCHES" ]]; then
  echo "ERROR: Dynamic Tailwind class interpolation detected (will be purged by JIT):"
  echo ""
  echo "$MATCHES"
  echo ""
  echo "Fix: replace template literals with a lookup object mapping variant → full class string."
  echo "Example:"
  echo "  // Bad:  \`bg-\${tone}-500\`"
  echo "  // Good: const toneClasses = { danger: 'bg-red-500', ... }[tone]"
  exit 1
fi

echo "No dynamic class interpolation found."
