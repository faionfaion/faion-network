#!/usr/bin/env bash
# purpose: Template helper for API OpenAPI Spec Authoring (openapi-bundle-check.sh).
# consumes: see content/02-output-contract.xml inputs for api-openapi-spec
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# openapi-bundle-check.sh — bundled output must match sources; then lint.
# Usage: ./openapi-bundle-check.sh [src-root] [output-file]
# Example: ./openapi-bundle-check.sh openapi/_root.yaml openapi.yaml
set -euo pipefail

SRC="${1:-openapi/_root.yaml}"
OUT="${2:-openapi.yaml}"
TMP=$(mktemp)

echo "Bundling $SRC → $TMP"
npx --yes @redocly/cli@latest bundle "$SRC" -o "$TMP" >/dev/null

echo "Checking $OUT is up-to-date..."
if ! diff -q "$TMP" "$OUT" >/dev/null; then
  echo "FAIL — $OUT is stale. Run: redocly bundle $SRC -o $OUT"
  diff -u "$OUT" "$TMP" | head -200
  exit 1
fi

echo "Running Spectral lint..."
npx --yes @stoplight/spectral-cli lint "$OUT" --fail-severity=warn

echo "Running Redocly lint..."
npx --yes @redocly/cli@latest lint "$OUT"

echo "Running oasdiff breaking-change check..."
if git rev-parse origin/main >/dev/null 2>&1; then
  git show origin/main:"$OUT" > /tmp/main-openapi.yaml 2>/dev/null || true
  if [ -f /tmp/main-openapi.yaml ]; then
    oasdiff breaking /tmp/main-openapi.yaml "$OUT" --fail-on ERR
  fi
fi

echo "OK"
