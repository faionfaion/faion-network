#!/usr/bin/env bash
# launch-pulse.sh — poll signup and visitor metrics every 5 minutes, post to Slack
#
# Required env vars:
#   SLACK_WEBHOOK    — Slack incoming webhook URL
#   PLAUSIBLE_TOKEN  — Plausible Analytics API token
#   SITE             — your-domain.com
#   SIGNUPS_API      — endpoint returning {"count": N} for today's signups
#
# Usage: bash launch-pulse.sh

set -euo pipefail

: "${SLACK_WEBHOOK:?set SLACK_WEBHOOK}"
: "${PLAUSIBLE_TOKEN:?set PLAUSIBLE_TOKEN}"
: "${SITE:?set SITE (e.g. your-domain.com)}"
: "${SIGNUPS_API:?set SIGNUPS_API (e.g. https://api.your-app.com/metrics/signups/today)}"

INTERVAL=300  # 5 minutes

while true; do
    signups=$(curl -sf "$SIGNUPS_API" | python3 -c "import sys,json; print(json.load(sys.stdin)['count'])" 2>/dev/null || echo "?")

    visitors=$(curl -sf \
        -H "Authorization: Bearer $PLAUSIBLE_TOKEN" \
        "https://plausible.io/api/v1/stats/aggregate?site_id=${SITE}&period=day&metrics=visitors" \
        | python3 -c "import sys,json; print(json.load(sys.stdin)['results']['visitors']['value'])" 2>/dev/null || echo "?")

    timestamp=$(date -u +%H:%MZ)
    msg="Launch pulse — visitors: ${visitors}, signups: ${signups} — ${timestamp}"

    curl -sf -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"${msg}\"}" "$SLACK_WEBHOOK" > /dev/null

    sleep "$INTERVAL"
done
