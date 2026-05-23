#!/usr/bin/env bash
# purpose: Shell helper that bulk-creates Jira issues from a CSV; consumed by the tool-selection rollout step.
# consumes: methodology inputs listed in AGENTS.md `## Prerequisites`
# produces: input for the artefact matching content/02-output-contract.xml
# depends-on: templates/header.yaml for frontmatter contract; AGENTS.md for body sections
# token-budget-impact: <300 tokens; CLI output piped to scripts/validate-<slug>.py

# Create Jira issues from a JSON work breakdown structure
# Requires: JIRA_URL, JIRA_TOKEN, JIRA_PROJECT_KEY env vars
# Input: JSON file path as first argument (or stdin)
# Usage: bash create-jira-issues.sh wbs.json

set -euo pipefail

ISSUES_FILE="${1:-/dev/stdin}"
ISSUES_JSON=$(cat "$ISSUES_FILE")

create_jira_issues() {
  echo "$ISSUES_JSON" | jq -c '.[]' | while IFS= read -r issue; do
    title=$(echo "$issue" | jq -r '.title')
    desc=$(echo "$issue" | jq -r '.description')
    type=$(echo "$issue" | jq -r '.type // "Story"' | sed 's/epic/Epic/;s/story/Story/;s/task/Task/;s/bug/Bug/')

    result=$(curl -s -w "\n%{http_code}" -X POST "$JIRA_URL/rest/api/3/issue" \
      -H "Authorization: Bearer $JIRA_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"fields\": {
          \"project\": {\"key\": \"$JIRA_PROJECT_KEY\"},
          \"summary\": \"$title\",
          \"description\": {
            \"type\": \"doc\", \"version\": 1,
            \"content\": [{\"type\": \"paragraph\",
              \"content\": [{\"text\": \"$desc\", \"type\": \"text\"}]}]
          },
          \"issuetype\": {\"name\": \"$type\"}
        }
      }")

    http_code=$(echo "$result" | tail -n1)
    body=$(echo "$result" | head -n-1)

    if [ "$http_code" != "201" ]; then
      echo "ERROR creating '$title': HTTP $http_code — $body" >&2
      exit 1
    fi

    key=$(echo "$body" | jq -r '.key')
    echo "Created: $key — $title"
    sleep 0.15  # stay under 10 req/sec Jira rate limit
  done
}

echo "Creating $(echo "$ISSUES_JSON" | jq length) Jira issues in project $JIRA_PROJECT_KEY..."
create_jira_issues
echo "Done."
