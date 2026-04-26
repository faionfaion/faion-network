#!/usr/bin/env bash
# api-first-check.sh — Lint OpenAPI spec with Spectral, then start Prism mock server.
# Usage: ./api-first-check.sh openapi.yaml [port]
# Output: lint report grouped by severity, then mock server on :PORT (default 4010)
# Requires: spectral, prism (npm install -g @stoplight/spectral-cli @stoplight/prism-cli)
set -euo pipefail

SPEC="${1:?Usage: $0 openapi.yaml [port]}"
PORT="${2:-4010}"

echo "--- Linting spec: $SPEC ---"
if [ -f ".spectral.yaml" ]; then
  spectral lint "$SPEC" --ruleset .spectral.yaml || { echo "Lint failed — fix errors before starting mock server"; exit 1; }
else
  spectral lint "$SPEC" || { echo "Lint failed — fix errors before starting mock server"; exit 1; }
fi

echo ""
echo "--- Starting Prism mock server on :$PORT ---"
echo "Test with: curl -s http://localhost:$PORT/resources | jq"
echo "Press Ctrl+C to stop"
prism mock "$SPEC" --port "$PORT"
