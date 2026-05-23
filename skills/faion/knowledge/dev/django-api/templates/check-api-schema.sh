#!/usr/bin/env bash
# purpose: CI step: validates Django views match drf-spectacular schema.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Add to CI workflow.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
# scripts/check-api-schema.sh
# Export OpenAPI schema and fail if breaking changes are detected vs docs/api/schema.yml.
# Run in CI or as a pre-commit hook.
set -euo pipefail

SCHEMA_FILE="docs/api/schema.yml"

python manage.py spectacular --file /tmp/schema.new.yml --fail-on-warn

if [ -f "$SCHEMA_FILE" ]; then
  if command -v oasdiff >/dev/null 2>&1; then
    oasdiff breaking "$SCHEMA_FILE" /tmp/schema.new.yml --fail-on ERR
  else
    diff -u "$SCHEMA_FILE" /tmp/schema.new.yml || {
      echo "OpenAPI schema changed. Update ${SCHEMA_FILE} or fix the regression." >&2
      exit 1
    }
  fi
fi

mkdir -p "$(dirname "$SCHEMA_FILE")"
mv /tmp/schema.new.yml "$SCHEMA_FILE"
echo "Schema updated: ${SCHEMA_FILE}"
