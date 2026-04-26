#!/usr/bin/env bash
# audit-to-backlog.sh — convert mlp-gap-finder JSON audit output into Linear issues
# Input:  audit.json (array of {feature, scores:{f,r,u,d}, pain, frequency, visibility})
# Output: Linear issues created via GraphQL API for features below MLP threshold
# Usage:  ./audit-to-backlog.sh audit.json TEAM_ID
# Requires: LINEAR_API_KEY env var, curl, jq
set -euo pipefail

AUDIT="${1:?Usage: audit-to-backlog.sh audit.json TEAM_ID}"
TEAM="${2:?Usage: audit-to-backlog.sh audit.json TEAM_ID}"
: "${LINEAR_API_KEY:?set LINEAR_API_KEY}"

jq -c '.[] | select(.scores.d < 4 or .scores.u < 4)' "$AUDIT" | while read -r row; do
  feature=$(echo "$row" | jq -r '.feature')
  layer=$(echo "$row" | jq -r 'if .scores.d < 4 then "delight" else "usable" end')
  pain=$(echo "$row" | jq -r '.pain // 3')
  freq=$(echo "$row" | jq -r '.frequency // 3')
  vis=$(echo "$row" | jq -r '.visibility // 3')
  prio=$((pain * freq * vis))

  curl -sS -X POST https://api.linear.app/graphql \
    -H "Authorization: $LINEAR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -nc \
          --arg t "$TEAM" \
          --arg title "MLP polish: $feature ($layer)" \
          --arg desc "Pain x Freq x Vis = $prio | Layer: $layer" \
          '{query:"mutation($i:IssueCreateInput!){issueCreate(input:$i){success issue{id}}}",
            variables:{i:{teamId:$t,title:$title,description:$desc,priority:2}}}')" \
    | jq -e '.data.issueCreate.success' >/dev/null
  echo "created: $feature (score=$prio, layer=$layer)"
done
