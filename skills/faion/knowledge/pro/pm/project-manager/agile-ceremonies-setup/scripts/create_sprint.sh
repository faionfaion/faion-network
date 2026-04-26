#!/usr/bin/env bash
# create_sprint.sh — create and start a Jira sprint via jira-cli.
# Usage: create_sprint.sh <PROJECT> <SPRINT_GOAL> [START_DATE] [END_DATE]
# Requires: jira-cli (ankitpokhrel/jira-cli), JIRA_AUTH_TOKEN env var.
set -euo pipefail

PROJECT="${1:?project key required}"
GOAL="${2:?sprint goal required}"
START="${3:-$(date -u +%F)}"
END="${4:-$(date -u -d '+14 days' +%F)}"

BOARD_ID=$(jira board --project "$PROJECT" --plain --no-headers --type scrum \
  | awk 'NR==1{print $1}')

SPRINT_ID=$(jira sprint create -b "$BOARD_ID" \
  -n "Sprint $(date -u +%G-W%V)" \
  -s "${START}T09:00" -e "${END}T17:00" \
  --plain | awk '{print $NF}')

# Move top 8 'Ready' issues into the sprint
jira sprint move -b "$BOARD_ID" -s "$SPRINT_ID" \
  $(jira issue list -p "$PROJECT" -s 'Ready' \
    --order-by priority --plain --no-headers \
    | awk '{print $1}' | head -8)

jira sprint start -b "$BOARD_ID" -s "$SPRINT_ID" --goal "$GOAL"
echo "Sprint $SPRINT_ID started: $GOAL"
