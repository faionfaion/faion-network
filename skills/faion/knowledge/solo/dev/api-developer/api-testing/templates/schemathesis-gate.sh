#!/usr/bin/env bash
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
