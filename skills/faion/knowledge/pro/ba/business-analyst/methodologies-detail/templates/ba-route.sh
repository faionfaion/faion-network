#!/usr/bin/env bash
# ba-route.sh — classify a BA request into the 12 BA frameworks, emit a deliverable checklist.
# Usage: ba-route.sh "We need to evaluate three vendor solutions"
#        echo "We need to assess the risks of the new system" | ba-route.sh
# Requires: ANTHROPIC_API_KEY in environment
set -euo pipefail
REQ="${1:-$(cat)}"

PROMPT=$(cat <<EOF
You are a BA technique classifier. Return ONLY JSON:
{
  "frameworks": ["framework-slug"],
  "babok_techniques": [technique_numbers],
  "rationale": "one sentence"
}
Frameworks (pick 1-3 maximum, require justification):
  governance, communication-planning, elicitation-prep,
  requirements-maintenance, change-impact, current-state, future-state,
  risk-analysis, change-strategy, requirements-architecture,
  solution-options, solution-limitations
Select at most 3 techniques from the BABOK 50 and justify each.
Request: """$REQ"""
EOF
)

JSON=$(curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" '{
    model: "claude-sonnet-4-5",
    max_tokens: 512,
    messages: [{"role": "user", "content": $p}]
  }')" | jq -r '.content[0].text')

echo "$JSON" | jq -r '.frameworks[]' | while read -r fw; do
  echo "- [ ] $fw → templates/${fw}.md"
done
echo ""
echo "BABOK techniques: $(echo "$JSON" | jq -r '.babok_techniques | join(", ")')"
echo "Rationale: $(echo "$JSON" | jq -r '.rationale')"
