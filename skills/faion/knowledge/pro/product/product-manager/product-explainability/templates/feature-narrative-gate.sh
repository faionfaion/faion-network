#!/usr/bin/env bash
# purpose: Gate script enforcing 90s + outcome-not-feature.
# consumes: input from methodology
# produces: artefact for downstream agent
# depends-on: content/02-output-contract.xml
# token-budget-impact: 0 (executes locally)
set -euo pipefail
#!/usr/bin/env bash
# feature-narrative-gate.sh — block release if narrative missing required fields or contains banned tokens.
# Usage: feature-narrative-gate.sh path/to/feature-narrative.json
# Exit: 0 = valid, 1 = validation failure
set -euo pipefail
fn="${1:?usage: feature-narrative-gate.sh NARRATIVE.json}"
schema="$(dirname "$0")/feature-narrative.schema.json"

cat > "$schema" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["purpose","behavior_change","measurable_outcome","limit","affected_personas"],
  "properties": {
    "purpose":{"type":"string","minLength":20,"maxLength":200},
    "behavior_change":{"type":"object",
      "required":["before","after"],
      "properties":{"before":{"type":"string"},"after":{"type":"string"}}},
    "measurable_outcome":{"type":"object",
      "required":["metric","baseline","current","isolation_method"],
      "properties":{"metric":{"type":"string"},"baseline":{"type":"string"},
                    "current":{"type":"string"},
                    "isolation_method":{"enum":["a/b","holdout","pre/post","unverified"]}}},
    "limit":{"type":"string","minLength":15},
    "affected_personas":{"type":"array","minItems":1,"items":{
      "type":"object","required":["name","job","value_received"]}},
    "risks":{"type":"array"}
  }
}
JSON

ajv validate -s "$schema" -d "$fn" --strict=true || exit 1

banned='best|leading|revolutionary|seamless|powerful|next-gen|delight|thrilled|excited|delighted'
if grep -E -i "\"($banned)\"" "$fn" >/dev/null; then
  echo "FAIL: banned marketing token in narrative"; exit 1
fi
echo "OK: feature-narrative.json passes all gates"
