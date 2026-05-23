# purpose: Shell helper computing AC coverage across stories.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env bash
# AC coverage: ratio of stories with AC linked.
set -euo pipefail
[ -f "${1:-}" ] || { echo 'usage: ac-coverage.sh <stories.json>'; exit 2; }
jq '{total: (.stories | length), with_ac: ([.stories[] | select(.acs | length > 0)] | length)}' "$1"
