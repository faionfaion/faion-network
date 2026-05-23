#!/usr/bin/env bash
# purpose: Shell helper to print KA → method list for a situation.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml (decision-record)
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as context
set -euo pipefail

echo "[knowledge-areas-detail] skeleton helper — replace with real logic."

# Example: list candidate frameworks for the current KA.
KA="${1:-KA-1}"
echo "KA: $KA"
