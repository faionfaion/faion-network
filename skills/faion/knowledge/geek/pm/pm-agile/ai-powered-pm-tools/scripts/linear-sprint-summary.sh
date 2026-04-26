#!/bin/bash
# linear-sprint-summary.sh — fetch active cycle tasks from Linear GraphQL API
# Usage: LINEAR_API_KEY=<key> ./linear-sprint-summary.sh <team_key>
# Output: JSON with cycle name, period, and issue list (title, state, assignee, priority)

TEAM_KEY="${1:?Usage: $0 <team_key>}"

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ team(key: \\\"$TEAM_KEY\\\") { activeCycle { name startsAt endsAt issues { nodes { title state { name } assignee { name } priority } } } } }\"}" | \
jq '.data.team.activeCycle | {
  cycle: .name,
  period: "\(.startsAt[:10]) to \(.endsAt[:10])",
  issues: [.issues.nodes[] | {title, state: .state.name, assignee: .assignee.name, priority}]
}'
