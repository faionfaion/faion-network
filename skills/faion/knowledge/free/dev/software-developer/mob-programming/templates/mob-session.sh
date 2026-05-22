#!/usr/bin/env bash
# purpose: start a mob session with visible timer + rotation prompts + draft PR.
# consumes: Done definition as $1; optional roster file.
# produces: stdout chimes + log of rotations + draft PR description.
# depends-on: bash, date, sleep, gh (optional).
# token-budget-impact: 0 — shell script.
# mob-session.sh — start a mob session with timer, scribe log, and draft PR.
# Usage: mob-session.sh "Add idempotency keys to /payments"
# Requires: mob (https://mob.sh), gh (GitHub CLI)
set -euo pipefail
goal="${1:?usage: mob-session.sh GOAL}"
slug=$(echo "$goal" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-' | cut -c1-40)
ts=$(date +%Y%m%d-%H%M)
log=".aidocs/mob/${ts}-${slug}.md"
mkdir -p "$(dirname "$log")"
cat > "$log" <<EOF
# Mob session: $goal
- Started: $(date -Is)
- Driver rotation: 10 min
- Roles: $(git config --get-all mob.participant 2>/dev/null | paste -sd, - || echo "unset")

## Decisions
## Parking lot
## Tests added
## Retro
EOF
git switch -c "mob/${slug}" 2>/dev/null || git switch "mob/${slug}"
mob start --branch "mob/${slug}" 10
gh pr create --draft --title "WIP mob: $goal" --body-file "$log" || true
( while true; do sleep 600; tput bel 2>/dev/null; echo "ROTATE"; done ) &
echo $! > /tmp/mob-timer.pid
echo "Log: $log  Timer PID: $(cat /tmp/mob-timer.pid)"
echo "End session: mob done && kill \$(cat /tmp/mob-timer.pid)"
