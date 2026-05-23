#!/usr/bin/env bash
# pm-scope-audit.sh — emit PM ticket-type distribution from Linear.
# Usage: GRAPHQL_TOKEN=... ./pm-scope-audit.sh <team-key> <since-iso>
# Output: TSV of pm_email, discovery_tickets, delivery_tickets, handoff_tickets
# Interpretation: PM at <20% discovery = delivery-broker (pre-blurring)
#                 PM at >50% discovery + nonzero handoff = AI-era target shape
#                 Pure handoff = role the Venn methodology says is dying.
set -euo pipefail
team="${1:?team-key required}"
since="${2:?since-iso required (e.g. 2026-01-01)}"
: "${GRAPHQL_TOKEN:?Linear API key required}"

q="{\"query\":\"query(\$t:String!,\$s:DateTimeOrDuration!){issues(filter:{team:{key:{eq:\$t}},updatedAt:{gt:\$s}}){nodes{assignee{email} labels{nodes{name}}}}}\",\"variables\":{\"t\":\"${team}\",\"s\":\"${since}\"}}"

curl -sS -X POST https://api.linear.app/graphql \
  -H "Authorization: $GRAPHQL_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$q" \
  | jq -r '
    .data.issues.nodes[]
    | select(.assignee.email)
    | {email: .assignee.email,
       kind: ([.labels.nodes[].name] | map(ascii_downcase)
              | if any(. == "discovery") then "discovery"
                elif any(. == "handoff" or . == "spec") then "handoff"
                else "delivery" end)}
    | [.email, .kind] | @tsv
  ' \
  | sort | uniq -c \
  | awk '{print $2"\t"$3"\t"$1}' \
  | sort
