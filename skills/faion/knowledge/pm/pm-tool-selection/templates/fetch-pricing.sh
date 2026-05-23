#!/usr/bin/env bash
# fetch-pricing.sh — snapshot PM tool pricing pages for diff-review.
# Run weekly via cron; commit snapshots to pricing-snapshots/ for change detection.
# Source: pm-tool-selection methodology.
set -euo pipefail

DEST="pricing-snapshots/$(date -u +%Y-%m-%d)"
mkdir -p "$DEST"

declare -A URLS=(
  [jira]="https://www.atlassian.com/software/jira/pricing"
  [linear]="https://linear.app/pricing"
  [clickup]="https://clickup.com/pricing"
  [notion]="https://www.notion.so/pricing"
  [asana]="https://asana.com/pricing"
  [monday]="https://monday.com/pricing"
  [github]="https://github.com/pricing"
  [gitlab]="https://about.gitlab.com/pricing/"
  [azure_devops]="https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/"
)

for tool in "${!URLS[@]}"; do
  curl -sSL --max-time 30 "${URLS[$tool]}" -o "$DEST/${tool}.html"
  echo "captured $tool"
done

git add "$DEST" && git commit -m "snapshot: PM pricing $(date -u +%F)"
