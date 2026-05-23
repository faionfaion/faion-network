# purpose: template for mob-programming (rotation-log.sh)
# consumes: mob-programming methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

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
