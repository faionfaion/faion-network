# purpose: Shell helper checking RACI has exactly one A per row.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env bash
# RACI lint: exactly one A per row.
set -euo pipefail
[ -f "${1:-}" ] || { echo 'usage: raci-lint.sh <raci.json>'; exit 2; }
jq -e 'all(.raci[]; (.accountable | type == "string" and length > 0))' "$1" >/dev/null \
  && echo 'OK: all rows have exactly one Accountable' || { echo 'FAIL'; exit 1; }
