#!/usr/bin/env bash
# purpose: CI step that regenerates the OpenAPI schema and fails on a breaking diff.
# consumes: a Django project with drf-spectacular configured; docs/api/schema.yml if committed.
# produces: an updated docs/api/schema.yml, or a non-zero exit on a breaking change.
# depends-on: content/01-core-rules.xml rule r10-openapi-generated.
# token-budget-impact: zero — local-only template; CI time is the only cost.

# Export the OpenAPI schema and fail if breaking changes appear vs docs/api/schema.yml.
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
