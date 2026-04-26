#!/usr/bin/env bash
# validate-flow.sh — fail if any onboarding step has no event mapping.
# Inputs:
#   flow.yaml   — steps[].id, steps[].event, steps[].required
#   events.yaml — events[].name (canonical event registry)
# Usage: ./validate-flow.sh flow.yaml events.yaml
set -euo pipefail

FLOW="${1:-flow.yaml}"
EVENTS="${2:-events.yaml}"

echo "Validating onboarding flow: $FLOW against event registry: $EVENTS"

yq -r '.steps[] | "\(.id) \(.event)"' "$FLOW" | while read -r step_id evt; do
  yq -e ".events[] | select(.name == \"$evt\")" "$EVENTS" > /dev/null \
    || { echo "MISSING event: step=$step_id event=$evt"; exit 1; }
  echo "  OK: step=$step_id event=$evt"
done

echo "OK: all flow steps map to defined events."
