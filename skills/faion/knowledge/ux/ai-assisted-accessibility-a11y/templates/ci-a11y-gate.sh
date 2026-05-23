# purpose: CI script invoking axe + pa11y and pushing artifacts to the Haiku filter.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

#!/usr/bin/env bash
# ci-a11y-gate.sh — Run pa11y-ci against a list of URLs; fail build on critical issues.
# Usage: ./ci-a11y-gate.sh [urls-file] [threshold]
#   urls-file: path to file with one URL per line (default: urls.txt)
#   threshold: max allowed errors before failure (default: 0 = fail on any error)
set -euo pipefail

URLS_FILE="${1:-urls.txt}"
THRESHOLD="${2:-0}"

pa11y-ci \
  --config .pa11yci.json \
  --threshold "$THRESHOLD" \
  $(cat "$URLS_FILE" | tr '\n' ' ')
