#!/usr/bin/env bash
# rotation-log.sh — append a rotation entry to MOB_LOG.md and trigger handoff.
# Usage: rotation-log.sh <driver> <navigator> [intent]
# Example: rotation-log.sh claude human "Validate the email format"
set -euo pipefail

DRIVER="${1:?driver required}"
NAV="${2:?navigator required}"
INTENT="${3:-}"
TS=$(date -u +%FT%TZ)

echo "- $TS  driver=$DRIVER  navigator=$NAV  intent=\"$INTENT\"" >> MOB_LOG.md

# Hand off via mob.sh if available
if command -v mob >/dev/null 2>&1; then
  mob next || true
fi

echo "Rotation logged. Next driver: $NAV"
