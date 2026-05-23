#!/usr/bin/env bash
# w3c-tokens-validate.sh — gate CI on W3C draft compliance
# Usage: bash w3c-tokens-validate.sh tokens.json
# Requires: ajv-cli (npm i -g ajv-cli), curl
set -euo pipefail

SCHEMA_URL="${SCHEMA_URL:-https://design-tokens.github.io/community-group/format/schema.json}"
FILE="${1:?Usage: w3c-tokens-validate.sh <tokens.json>}"

echo "Fetching W3C draft schema..."
curl -sSL "$SCHEMA_URL" -o /tmp/dt.schema.json

echo "Validating $FILE..."
ajv validate -s /tmp/dt.schema.json -d "$FILE" --strict=false \
  || { echo "FAIL: $FILE is not W3C-compliant"; exit 1; }

echo "OK: $FILE conforms to W3C draft"
