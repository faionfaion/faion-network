#!/bin/bash
# Fetch AI Overview performance data from Google Search Console API
# Requires: gcloud auth application-default login
# Usage: ./gsc-fetch.sh <site_url> [start_date] [end_date]
# Output: JSON with query, page, clicks, impressions per row

SITE_URL="${1:?Usage: $0 <site_url> <start_date> <end_date>}"
START="${2:-2025-06-01}"
END="${3:-2025-12-31}"

ACCESS_TOKEN=$(gcloud auth application-default print-access-token)
ENCODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITE_URL', safe=''))")

curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/${ENCODED_URL}/searchAnalytics/query" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"startDate\": \"$START\",
    \"endDate\": \"$END\",
    \"dimensions\": [\"query\", \"page\"],
    \"searchType\": \"discover\"
  }" | jq '.rows[] | {
    query: .keys[0],
    page: .keys[1],
    clicks: .clicks,
    impressions: .impressions,
    ctr: .ctr,
    position: .position
  }'
