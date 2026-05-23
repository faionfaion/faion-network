#!/usr/bin/env bash
# apply-workflow.sh — push workflow JSON to a Jira Cloud sandbox project via REST API
# Usage: apply-workflow.sh <PROJECT_KEY> <workflow.json>
# Env:   JIRA_BASE, JIRA_USER, JIRA_TOKEN
set -euo pipefail

: "${JIRA_BASE:?JIRA_BASE must be set (e.g. https://yoursite.atlassian.net)}"
: "${JIRA_USER:?JIRA_USER must be set (e.g. bot@company.com)}"
: "${JIRA_TOKEN:?JIRA_TOKEN must be set (Jira API token)}"

PROJECT_KEY="${1:?usage: apply-workflow.sh <PROJECT_KEY> <workflow.json>}"
WF="${2:?usage: apply-workflow.sh <PROJECT_KEY> <workflow.json>}"

echo "Pushing workflow from $WF to $JIRA_BASE..."
WORKFLOW_ID=$(curl -fsSL \
  -u "$JIRA_USER:$JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "$JIRA_BASE/rest/api/3/workflows/create" \
  -d @"$WF" | jq -r '.id')

echo "Created workflow ID: $WORKFLOW_ID"
echo "Next: associate workflow $WORKFLOW_ID with project $PROJECT_KEY"
echo "  - Via UI: Project Settings > Workflows > Scheme > Add Workflow"
echo "  - Via API: /rest/api/3/workflowscheme (requires admin)"
