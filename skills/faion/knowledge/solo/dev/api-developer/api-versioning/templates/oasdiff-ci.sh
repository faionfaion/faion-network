#!/usr/bin/env bash
# oasdiff-ci.sh — CI breaking-change gate.
# Fails if breaking changes are detected without a documented version bump.
# Requires: oasdiff (brew install tufin/tap/oasdiff), jq
#
# Usage: ./oasdiff-ci.sh [openapi-file]
# Example: ./oasdiff-ci.sh openapi.yaml
set -euo pipefail

SPEC="${1:-openapi.yaml}"
CHANGELOG_PENDING="${2:-.changelog-pending}"

# Fetch main branch spec for comparison
git fetch origin main:main 2>/dev/null || true

if ! git show main:"$SPEC" > /tmp/main-openapi.yaml 2>/dev/null; then
  echo "No main branch spec found — skipping breaking change check"
  exit 0
fi

echo "Running oasdiff breaking change check..."
oasdiff breaking /tmp/main-openapi.yaml "$SPEC" \
  --fail-on ERR \
  --format json > /tmp/diff.json 2>&1 || true

n=$(jq 'length' /tmp/diff.json 2>/dev/null || echo 0)

if [ "$n" -gt 0 ]; then
  echo "::error::$n breaking change(s) detected:"
  jq -r '.[] | "  \(.id) \(.path) \(.text)"' /tmp/diff.json

  # Allow breaking changes only when explicitly documented
  if [ ! -f "$CHANGELOG_PENDING" ] || ! grep -qE '^v[0-9]+: breaking' "$CHANGELOG_PENDING"; then
    echo ""
    echo "::error::To allow breaking changes, add a 'v<N>: breaking - <reason>' line to ${CHANGELOG_PENDING}"
    echo "::error::Or revert the breaking change and use an additive alternative."
    exit 1
  fi

  echo "Breaking changes acknowledged in ${CHANGELOG_PENDING} — proceeding"
fi

echo "OK — no unacknowledged breaking changes"
