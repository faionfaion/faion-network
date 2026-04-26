#!/bin/bash
# Create a Linear issue via GraphQL mutation
# Usage: LINEAR_KEY=<key> TEAM_ID=<id> bash create-issue.sh "Title" "Description" "High"

TITLE="$1"
DESC="$2"
PRIORITY="$3"  # Urgent | High | Medium | Low | NoPriority

priority_int() {
  case "$1" in
    Urgent)     echo 1 ;;
    High)       echo 2 ;;
    Medium)     echo 3 ;;
    Low)        echo 4 ;;
    *)          echo 0 ;;  # NoPriority
  esac
}

P=$(priority_int "$PRIORITY")

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { issueCreate(input: { teamId: \\\"$TEAM_ID\\\", title: \\\"$TITLE\\\", description: \\\"$DESC\\\", priority: $P }) { success issue { id identifier url } } }\"}" \
  | jq '.data.issueCreate.issue | {id, identifier, url}'
