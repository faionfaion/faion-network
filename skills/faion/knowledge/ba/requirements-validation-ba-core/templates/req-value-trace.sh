# purpose: Shell helper linking requirements to value drivers.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env bash
# Trace requirements to value drivers; emit JSON.
set -euo pipefail
[ -f "${1:-}" ] || { echo 'usage: req-value-trace.sh <requirements.json>'; exit 2; }
jq '[.requirements[] | {req_id, value_drivers}]' "$1"
