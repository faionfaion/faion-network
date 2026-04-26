#!/bin/bash
# linear-to-spec.sh — scaffold spec.md from a Linear issue
# Usage: LINEAR_API_KEY=<key> ./linear-to-spec.sh <ISSUE_ID>
# Requires: curl, jq

ISSUE_ID="${1:?Usage: $0 <ISSUE_ID>}"
API_KEY="${LINEAR_API_KEY:?LINEAR_API_KEY not set}"

ISSUE=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ issue(id: \\\"$ISSUE_ID\\\") { title description priority labels { nodes { name } } } }\"}")

TITLE=$(echo "$ISSUE" | jq -r '.data.issue.title')
DESC=$(echo "$ISSUE" | jq -r '.data.issue.description // "No description provided"')

cat <<EOF
# Spec: $TITLE

## Metadata
| Field | Value |
|-------|-------|
| Status | Draft |
| Linear Issue | $ISSUE_ID |

## Intent (from Linear)
$DESC

## Functional Requirements
<!-- AI: generate FR-1..N from intent above -->

## Non-Goals (Out of Scope)
<!-- Required: list what this spec does NOT cover -->

## Edge Cases
| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-1 | | |

## Acceptance Criteria
<!-- Given-When-Then for each FR -->

## Assumptions
<!-- List assumptions made due to missing information -->
EOF
