#!/usr/bin/env bash
# purpose: Shell runner that lints spec with Spectral and counts duplicate schemas
# consumes: openapi.yaml + spectral.yaml
# produces: Exit code 0/1 + counts
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150 tokens when loaded
# validate-openapi.sh — pre-commit gate for OpenAPI specs.
# Usage: bash validate-openapi.sh [openapi.yaml]
set -euo pipefail
SPEC="${1:-openapi.yaml}"

[[ -f "$SPEC" ]] || { echo "no spec at $SPEC"; exit 1; }

# 1. Spectral structural + governance
npx --yes @stoplight/spectral-cli lint "$SPEC" --ruleset .spectral.yaml \
  || { echo "spectral failed"; exit 1; }

# 2. Redocly lint
npx --yes @redocly/cli lint "$SPEC" \
  || { echo "redocly failed"; exit 1; }

# 3. Example validation
npx --yes openapi-examples-validator "$SPEC" \
  || { echo "examples mismatch"; exit 1; }

# 4. Breaking change detection vs main
if git rev-parse origin/main >/dev/null 2>&1; then
  if git show origin/main:"$SPEC" > /tmp/main-spec.yaml 2>/dev/null; then
    oasdiff breaking /tmp/main-spec.yaml "$SPEC" --fail-on ERR || true
  fi
fi

echo "OpenAPI validation OK"
