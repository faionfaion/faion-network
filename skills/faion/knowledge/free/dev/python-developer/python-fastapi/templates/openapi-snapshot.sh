#!/usr/bin/env bash
# purpose: Generate and diff openapi.json against committed snapshot
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# openapi-snapshot.sh — diff served openapi.json against committed snapshot.
# Fails (exit 1) if schema changed, moves new version into place for review.
# Usage: bash scripts/openapi-snapshot.sh
set -euo pipefail

python - <<'PY' > openapi.new.json
import json
from app.main import app
print(json.dumps(app.openapi(), indent=2, sort_keys=True))
PY

if [[ -f openapi.json ]]; then
    if diff -u openapi.json openapi.new.json; then
        rm openapi.new.json
        echo "OK — openapi.json is up to date"
        exit 0
    fi
    echo ""
    echo "OpenAPI schema changed. Review the diff above."
    echo "If intentional, commit openapi.new.json as openapi.json."
    mv openapi.new.json openapi.json
    exit 1
fi

# First run — create the snapshot
mv openapi.new.json openapi.json
echo "Created openapi.json snapshot — commit this file."
