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
