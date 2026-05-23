#!/usr/bin/env bash
# purpose: Template helper for API Testing (schemathesis-gate.sh).
# consumes: see content/02-output-contract.xml inputs for api-testing
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# Schemathesis fuzz CI gate.
# Input: $1 = app base URL (e.g. http://localhost:8000)
# Output: JUnit XML report at reports/schemathesis.xml
# Usage: bash schemathesis-gate.sh http://localhost:8000
set -euo pipefail

APP=${1:?usage: $0 <app-base-url>}

schemathesis run "$APP/openapi.json" \
  --checks all \
  --hypothesis-max-examples=50 \
  --workers 4 \
  --header "Authorization: Bearer $TEST_TOKEN" \
  --junit-xml=reports/schemathesis.xml
