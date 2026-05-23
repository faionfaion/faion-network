#!/usr/bin/env bash
# purpose: Classify a BA request into BABOK knowledge areas, list candidate methodologies
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml (decision-record)
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-800 tokens when loaded as context

# ba-route.sh — classify a BA request into BABOK knowledge areas, list candidate methodologies.
# Usage: echo "we need to figure out why churn is up" | ba-route.sh
#        ba-route.sh "user request text"
# Requires: ANTHROPIC_API_KEY in environment
set -euo pipefail

REQ="${1:-$(cat)}"
KB="skills/faion/knowledge/pro/ba"

PROMPT=$(cat <<EOF
You are a BABOK KA router. Read the request and respond with JSON only:
{
  "primary_ka": "KA-N",
  "secondary_kas": ["KA-M"],
  "methodologies": ["slug-1", "slug-2"],
  "missing_inputs": ["what is needed before work can start"]
}
Rules:
- Never invent KAs outside KA-1..KA-6.
- KA-1: planning, KA-2: elicitation, KA-3: lifecycle, KA-4: strategy, KA-5: analysis-design, KA-6: evaluation.
- If KA-6 is selected and no telemetry source is provided, list it under missing_inputs and stop.
- Allowed methodologies (pick from):
  KA-1: ba-planning, stakeholder-analysis
  KA-2: elicitation-techniques
  KA-3: requirements-traceability, requirements-lifecycle, requirements-prioritization
  KA-4: strategy-analysis
  KA-5: requirements-documentation, business-process-analysis, use-case-modeling,
         user-story-mapping, acceptance-criteria, requirements-validation,
         decision-analysis, data-analysis, interface-analysis
  KA-6: solution-assessment
Request: $REQ
EOF
)

curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" '{
    model: "claude-opus-4-5",
    max_tokens: 1024,
    messages: [{"role": "user", "content": $p}]
  }')" | jq -r '.content[0].text'
