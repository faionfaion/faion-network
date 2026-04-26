#!/bin/bash
# Count deployments in last 30 days from GitHub releases
# Usage: bash dora-deployment-count.sh <owner/repo>
# Requires: gh CLI authenticated

REPO="${1:?Usage: $0 <owner/repo>}"
THIRTY_DAYS_AGO=$(date -d '30 days ago' --iso-8601=seconds)

COUNT=$(gh api "repos/$REPO/releases" \
  --jq "[.[] | select(.created_at > \"$THIRTY_DAYS_AGO\")] | length" \
  --paginate | paste -sd+ | bc)

echo "$COUNT deployments in last 30 days for $REPO"
echo "Deployment frequency: $(echo "scale=2; $COUNT / 30" | bc) per day"
