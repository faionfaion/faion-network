#!/usr/bin/env bash
# purpose: one-liner filters for inspecting an existing stream-json replay file with jq
# consumes: runs/<session_id>.jsonl
# produces: filtered stdout per filter mode
# depends-on: jq >= 1.6 on PATH; bash >= 4
# token-budget-impact: ~120 tokens to render

set -euo pipefail

FILE="${1:-}"
MODE="${2:-assistant}"

if [ -z "${FILE}" ] || [ "${FILE}" = "--help" ]; then
  cat <<EOF
Usage: $0 <replay.jsonl> [assistant|tools|cost|errors|all]
  assistant   only assistant message text (default)
  tools       all tool_use events with name + input
  cost        running total_cost_usd per event
  errors      result events with non-success subtype
  all         pretty-print every event
EOF
  exit 0
fi

case "${MODE}" in
  assistant)
    jq -c 'select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text' "${FILE}"
    ;;
  tools)
    jq -c 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | {name, input}' "${FILE}"
    ;;
  cost)
    jq -c 'select(.total_cost_usd != null) | {t: .type, cost: .total_cost_usd}' "${FILE}"
    ;;
  errors)
    jq -c 'select(.type == "result" and .subtype != "success")' "${FILE}"
    ;;
  all)
    jq '.' "${FILE}"
    ;;
  *)
    echo "unknown mode: ${MODE}" >&2
    exit 2
    ;;
esac
