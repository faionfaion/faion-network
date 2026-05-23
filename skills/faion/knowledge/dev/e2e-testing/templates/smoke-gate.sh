#!/usr/bin/env bash
# purpose: deploy gate — block release if @smoke E2E fails against the staging URL.
# consumes: BASE_URL (required), TIMEOUT (default 300s), SMOKE_TAG (default @smoke).
# produces: exit 0 on pass, non-zero on fail; playwright-report/ HTML artefact.
# depends-on: npx, @playwright/test installed in the project.
# token-budget-impact: 0 — shell script, not loaded into LLM context at runtime.
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
