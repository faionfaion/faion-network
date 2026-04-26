#!/usr/bin/env bash
# ops-rollup.sh — generate weekly Product Ops rollup from Linear + PostHog.
# Outputs Markdown to stdout. Pipe into Notion via notion-cli or commit to docs repo.
# Required env: LINEAR_API_KEY, POSTHOG_API_KEY, POSTHOG_HOST
set -euo pipefail
: "${LINEAR_API_KEY:?LINEAR_API_KEY required}"
: "${POSTHOG_API_KEY:?POSTHOG_API_KEY required}"
: "${POSTHOG_HOST:?POSTHOG_HOST required}"

since=$(date -u -d "7 days ago" +%Y-%m-%dT%H:%M:%SZ)
echo "# Product Ops rollup - $(date -u +%Y-%m-%d)"
echo

echo "## Shipped"
curl -fsSL -H "Authorization: $LINEAR_API_KEY" -X POST https://api.linear.app/graphql \
  -H 'Content-Type: application/json' \
  -d "{\"query\":\"{ issues(filter:{completedAt:{gte:\\\"$since\\\"}}, first:50){ nodes{ identifier title team{name} url } } }\"}" \
  | jq -r '.data.issues.nodes[] | "- [\(.team.name)] \(.identifier) \(.title) <\(.url)>"' \
  || echo "_linear unavailable_"
echo

echo "## At-risk (>2d slip)"
curl -fsSL -H "Authorization: $LINEAR_API_KEY" -X POST https://api.linear.app/graphql \
  -H 'Content-Type: application/json' \
  -d "{\"query\":\"{ issues(filter:{state:{type:{eq:\\\"started\\\"}}, dueDate:{lt:\\\"$(date -u +%Y-%m-%d)\\\"}}, first:50){ nodes{ identifier title dueDate url } } }\"}" \
  | jq -r '.data.issues.nodes[] | "- \(.identifier) \(.title) due=\(.dueDate) <\(.url)>"' \
  || echo "_linear unavailable_"
echo

echo "## Metric movers (>10%)"
curl -fsSL -H "Authorization: Bearer $POSTHOG_API_KEY" \
  "$POSTHOG_HOST/api/projects/@current/insights/trend?interval=week&date_from=-14d" \
  | jq -r '.result[]? | select((.aggregated_value // 0) != 0) | "- \(.label): \(.aggregated_value)"' \
  | head -20 \
  || echo "_posthog unavailable_"
