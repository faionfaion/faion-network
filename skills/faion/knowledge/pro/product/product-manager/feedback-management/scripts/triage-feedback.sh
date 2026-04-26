#!/usr/bin/env bash
# triage-feedback.sh — categorize feedback items via Claude Haiku
# Input:  stdin, one item per line: ISO_DATE\tSOURCE\tUSER_ID\tVERBATIM
# Output: JSONL to stdout, one JSON object per item
# Usage:  cat feedback.txt | ./triage-feedback.sh > triaged.jsonl
# Requires: ANTHROPIC_API_KEY env var, curl, jq
set -euo pipefail
: "${ANTHROPIC_API_KEY:?set ANTHROPIC_API_KEY}"

SYSTEM='You are a feedback triage agent. Output ONLY one JSON object, no prose.
Schema: {"type":"bug|request|enhancement|confusion|praise|complaint",
"topic":"onboarding|core-A|core-B|billing|integrations|performance|other",
"segment":"free|solo|pro|geek|unknown",
"sentiment":"positive|neutral|negative",
"confidence":0.0,
"action_required":"build|wont_do|need_info|already_planned"}
Rules:
- Use ONLY the exact enum values above. Never invent new tags.
- If confidence < 0.7 set action_required="need_info".
- If topic is ambiguous, prefer "other" over an incorrect specific tag.'

while IFS=$'\t' read -r date source user verbatim; do
  body=$(jq -nc --arg s "$SYSTEM" --arg u "Date:$date Source:$source User:$user Verbatim:$verbatim" \
    '{model:"claude-haiku-4-5", max_tokens:300, system:$s, messages:[{role:"user", content:$u}]}')
  resp=$(curl -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$body" | jq -r '.content[0].text')
  jq -nc --argjson t "$resp" --arg d "$date" --arg s "$source" --arg u "$user" --arg v "$verbatim" \
    '{date:$d, source:$s, user:$u, verbatim:$v} + $t'
done
