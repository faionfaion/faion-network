#!/usr/bin/env bash
# purpose: CI gate that regenerates TS DTOs from Go and fails the build on uncommitted drift.
# consumes: tygo.yaml + Go source packages listed in it.
# produces: config (regenerated web/src/types/api.ts diff check).
# depends-on: content/02-output-contract.xml; templates/tygo.yaml.
# token-budget-impact: low — ~120 tokens.
# CI gate: regenerate TS DTOs from Go and assert no drift.
# Run via:  bash templates/ci-check.sh
set -euo pipefail

OUT=web/src/types/api.ts

go run github.com/gzuidhof/tygo@latest generate -config tygo.yaml

if ! git diff --exit-code -- "$OUT"; then
  echo "ERROR: $OUT is out of date. Run 'tygo generate' and commit the result." >&2
  exit 1
fi

# Reject untyped escape hatches.
if grep -nE ':\s*any[;,]' "$OUT"; then
  echo "ERROR: generated TS contains 'any' — add a type_mapping to tygo.yaml." >&2
  exit 1
fi
