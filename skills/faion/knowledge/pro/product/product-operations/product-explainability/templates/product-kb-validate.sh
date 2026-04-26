#!/usr/bin/env bash
# product-kb-validate.sh — validate product-kb.json against JSON Schema.
# Usage: product-kb-validate.sh path/to/product-kb.json
# Wire into pre-commit so releases cannot ship a KB missing limits, deprecated-status flags, or audience.
# Requires: ajv-cli (npm i -g ajv-cli)
set -euo pipefail
kb="${1:?usage: product-kb-validate.sh KB.json}"
schema="$(dirname "$0")/product-kb.schema.json"
cat > "$schema" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["purpose","capabilities","limits","use_cases","audience"],
  "properties": {
    "purpose": {"type":"string","minLength":20,"maxLength":240},
    "capabilities": {"type":"array","minItems":3,"items":{
      "type":"object",
      "required":["name","description","status","since_version"],
      "properties":{
        "name":{"type":"string"},
        "description":{"type":"string","minLength":20},
        "example":{"type":"string"},
        "status":{"enum":["ga","beta","deprecated"]},
        "since_version":{"type":"string"}}}},
    "limits": {"type":"array","minItems":3,"items":{
      "type":"object",
      "required":["scope","rationale"],
      "properties":{
        "scope":{"type":"string"},
        "rationale":{"type":"string"},
        "workaround":{"type":["string","null"]}}}},
    "use_cases": {"type":"array","minItems":2},
    "audience": {"type":"object",
      "required":["industry","role"],
      "properties":{
        "industry":{"type":"string"},
        "role":{"type":"string"},
        "company_size":{"type":"string"}}}
  }
}
JSON
ajv validate -s "$schema" -d "$kb" --strict=true
echo "OK: $kb is valid."
