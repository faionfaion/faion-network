#!/usr/bin/env bash
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
