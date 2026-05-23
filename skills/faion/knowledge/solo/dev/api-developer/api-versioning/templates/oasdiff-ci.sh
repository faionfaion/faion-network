#!/usr/bin/env bash
# __faion_header_v1__
# purpose: CI breaking-change gate: oasdiff diff + .changelog-pending enforcement
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#additive-first
# faion_header_json: {"__faion_header__":{"purpose":"CI breaking-change gate: oasdiff diff + .changelog-pending enforcement","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#additive-first","token_budget_impact":"~150 tokens when loaded"}}
set -euo pipefail
SPEC="${1:-openapi.yaml}"
CHANGELOG_PENDING="${2:-.changelog-pending}"
git fetch origin main:main 2>/dev/null || true
if ! git show main:"$SPEC" > /tmp/main-openapi.yaml 2>/dev/null; then
  echo "No main branch spec; skipping breaking-change check"
  exit 0
fi
oasdiff breaking /tmp/main-openapi.yaml "$SPEC" --fail-on ERR --format json > /tmp/diff.json 2>&1 || true
n=$(jq 'length' /tmp/diff.json 2>/dev/null || echo 0)
if [ "$n" -gt 0 ]; then
  jq -r '.[] | "  \(.id) \(.path) \(.text)"' /tmp/diff.json
  if [ ! -f "$CHANGELOG_PENDING" ] || ! grep -qE '^v[0-9]+: breaking' "$CHANGELOG_PENDING"; then
    echo "breaking change without changelog-pending bump" >&2
    exit 1
  fi
fi
echo "OK"
