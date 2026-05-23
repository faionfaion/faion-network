#!/usr/bin/env bash
# purpose: Scaffold a new sprint folder + draft sprint plan
# consumes: sprint number argument
# produces: sprint folder with planning + retro templates copied
# depends-on: content/01-core-rules.xml
# token-budget-impact: 0 (CLI script, not a prompt)
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <sprint-number>" >&2
  exit 2
fi

SPRINT="sprint-$1"
mkdir -p "$SPRINT"
cp templates/sprint-planning.md "$SPRINT/planning.md"
cp templates/retrospective.md "$SPRINT/retro.md"
echo "Scaffolded $SPRINT"
