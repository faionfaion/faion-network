#!/usr/bin/env bash
# smoke-gate.sh — block deploy if smoke E2E fails on staging URL.
# Usage: BASE_URL=https://staging.example.com bash smoke-gate.sh
set -euo pipefail
BASE_URL="${BASE_URL:?BASE_URL required}"
TIMEOUT="${TIMEOUT:-300}"
SMOKE_TAG="${SMOKE_TAG:-@smoke}"

echo "smoke against $BASE_URL"
npx playwright install --with-deps chromium >/dev/null

timeout "${TIMEOUT}" npx playwright test \
  --project=chromium \
  --grep "${SMOKE_TAG}" \
  --reporter=list,html \
  --workers=2 \
  || { echo "smoke FAILED — see playwright-report/"; exit 1; }

echo "smoke OK"
