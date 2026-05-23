#!/usr/bin/env bash
# market-share-proxy.sh — assemble share-estimation proxies into one CSV row.
# Usage: ./market-share-proxy.sh <slug> <domain> <crunchbase_uuid>
# Requires: SIMILARWEB_KEY, CRUNCHBASE_KEY env vars; gh CLI installed.
set -euo pipefail

SLUG="$1"; DOMAIN="$2"; CB_UUID="${3:-}"
Q="$(date +%Y)Q$(( ($(date +%-m)-1)/3+1 ))"
OUT="./_portfolio/${Q}.csv"
mkdir -p "$(dirname "$OUT")"
[ -f "$OUT" ] || echo "quarter,slug,domain,traffic_visits,employees,gh_stars,pricing_changes,funding_usd" > "$OUT"

traffic=$(curl -fsSL \
  "https://api.similarweb.com/v1/website/$DOMAIN/total-traffic-and-engagement/visits?api_key=$SIMILARWEB_KEY&granularity=monthly" \
  | jq -r '[.visits[].visits] | add // "unknown"' 2>/dev/null || echo unknown)

emp=$(curl -fsSL -H "X-cb-user-key: $CRUNCHBASE_KEY" \
  "https://api.crunchbase.com/api/v4/entities/organizations/$CB_UUID?field_ids=num_employees_enum" \
  | jq -r '.properties.num_employees_enum // "unknown"' 2>/dev/null || echo unknown)

stars=$(gh api "search/repositories?q=user:$SLUG" \
  --jq '[.items[].stargazers_count]|add // "unknown"' 2>/dev/null || echo unknown)

funding=$(curl -fsSL -H "X-cb-user-key: $CRUNCHBASE_KEY" \
  "https://api.crunchbase.com/api/v4/entities/organizations/$CB_UUID?field_ids=funding_total" \
  | jq -r '.properties.funding_total.value_usd // "unknown"' 2>/dev/null || echo unknown)

pricing_changes=$(waybackpack -d /tmp/wb "https://$DOMAIN/pricing" --from-date 2023 2>/dev/null \
  | wc -l || echo unknown)

echo "$Q,$SLUG,$DOMAIN,$traffic,$emp,$stars,$pricing_changes,$funding" >> "$OUT"
echo "row appended for $SLUG in $OUT"
