#!/usr/bin/env bash
# pm-ops-contract-check.sh — refuse PM-side write attempts to system-of-record.
# Wrap PM agent invocations: if the planned action touches a write surface
# owned by Product Ops, exit non-zero and instruct the agent to use the
# hand-off queue instead.
# Usage: pm-ops-contract-check.sh <planned-action.json>
# planned-action.json format: {"calls": [{"op": "write", "target": "linear"}]}
set -euo pipefail
ACTION="${1:?usage: pm-ops-contract-check.sh <planned-action.json>}"
# Systems where Product Ops owns write access
WRITE_OWNED_BY_OPS='linear|jira|productboard|aha|notion-canonical|dbt-models|kpi-dictionary'

if jq -e --arg p "$WRITE_OWNED_BY_OPS" '
  .calls[] | select(.op == "write") | .target | test($p)
' "$ACTION" >/dev/null 2>&1; then
  echo "BLOCKED: PM agent attempted Product-Ops-owned write."
  echo "Hand-off path: post to #product-ops-intake or open PR in ops/templates."
  echo "Systems owned by Product Ops: linear, jira, productboard, aha, notion-canonical, dbt-models, kpi-dictionary"
  exit 2
fi
echo "OK: PM agent stays within read + narrative scope."
