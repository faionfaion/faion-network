#!/usr/bin/env bash
# interface-drift-check.sh — flag breaking changes between committed spec and live API.
# Usage: ./interface-drift-check.sh <committed-openapi.yaml> <live-openapi-url>
# Exit: 0 = in sync, 2 = breaking change detected
# Requirements: npx (Node), oasdiff (go install github.com/oasdiff/oasdiff@latest)
set -euo pipefail
COMMITTED="${1:?committed spec path required}"
LIVE_URL="${2:?live OpenAPI URL required}"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

curl -fsSL "$LIVE_URL" -o "$WORK/live.yaml"

# Lint both sides
npx --yes @redocly/cli lint "$COMMITTED" >/dev/null
npx --yes @redocly/cli lint "$WORK/live.yaml" >/dev/null

# Breaking-change diff (exits non-zero on breaking change)
oasdiff breaking "$COMMITTED" "$WORK/live.yaml" --fail-on ERR > "$WORK/diff.txt" || {
  echo "BREAKING CHANGE detected between $COMMITTED and $LIVE_URL:"
  cat "$WORK/diff.txt"
  echo ""
  echo "Action: review diff, update IF-XXX spec, and open SDD task under todo/"
  exit 2
}

# Non-breaking changelog (informational)
oasdiff changelog "$COMMITTED" "$WORK/live.yaml" > "$WORK/changes.md" || true
echo "Spec in sync with live API."
if [[ -s "$WORK/changes.md" ]]; then
  echo "Non-breaking changes (informational):"
  cat "$WORK/changes.md"
fi
