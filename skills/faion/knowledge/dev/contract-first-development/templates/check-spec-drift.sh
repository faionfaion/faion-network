#!/usr/bin/env bash
# purpose: CI gate that fails on spec/code drift or breaking schema changes
# consumes: openapi.yaml + server/app/models + git main branch spec
# produces: pass/fail exit code (0=clean, 1=drift or breaking change)
# depends-on: spectral, openapi-generator-cli, oasdiff, redocly
# token-budget-impact: ~300 tokens when loaded as context
# check-spec-drift.sh — fail CI if generated code diverges from server/ or spec has breaking changes.
# Usage: bash check-spec-drift.sh [openapi.yaml]
set -euo pipefail

SPEC="${1:-openapi.yaml}"
GENERATED_DIR=$(mktemp -d)

# 1. Lint spec
redocly lint "$SPEC" || { echo "redocly lint failed"; exit 1; }
npx --yes @stoplight/spectral-cli lint "$SPEC" --ruleset .spectral.yaml \
  || { echo "spectral lint failed"; exit 1; }

# 2. Generate stubs and diff against committed server models
openapi-generator-cli generate \
  -i "$SPEC" -g python-fastapi -o "$GENERATED_DIR" \
  --additional-properties=packageName=app

DIFF=$(diff -r --brief "$GENERATED_DIR/app/models" server/app/models 2>&1 || true)
if [[ -n "$DIFF" ]]; then
  echo "Spec vs implementation drift detected:"
  echo "$DIFF"
  echo "Run: cp -r $GENERATED_DIR/app/models server/app/models"
  exit 1
fi

# 3. Breaking change check vs main branch
git fetch origin main:main 2>/dev/null || true
if git show main:"$SPEC" > /tmp/spec-main.yaml 2>/dev/null; then
  oasdiff breaking /tmp/spec-main.yaml "$SPEC" --fail-on ERR
fi

echo "Spec drift check OK"
