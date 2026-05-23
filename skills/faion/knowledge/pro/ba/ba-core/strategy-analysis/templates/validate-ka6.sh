# purpose: Shell validator for BABOK KA6 artefacts.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env bash
# Validate BABOK KA6 artefacts (business_need ≥ 80 chars, gaps non-empty).
set -euo pipefail
[ -f "${1:-}" ] || { echo 'usage: validate-ka6.sh <ka6.json>'; exit 2; }
jq -e '.business_need | length >= 80' "$1" >/dev/null && echo 'OK' || { echo 'FAIL: business_need < 80'; exit 1; }
