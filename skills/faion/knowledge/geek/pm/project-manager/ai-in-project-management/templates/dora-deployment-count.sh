#!/usr/bin/env bash
# purpose: Shell helper that counts deploys against a Git remote for a date range; feeds the DORA baseline metric.
# consumes: methodology inputs listed in AGENTS.md `## Prerequisites`
# produces: input for the artefact matching content/02-output-contract.xml
# depends-on: templates/header.yaml for frontmatter contract; AGENTS.md for body sections
# token-budget-impact: <300 tokens; CLI output piped to scripts/validate-<slug>.py

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
