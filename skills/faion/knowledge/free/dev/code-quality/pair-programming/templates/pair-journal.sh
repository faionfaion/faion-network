# purpose: template for pair-programming (pair-journal.sh)
# consumes: pair-programming methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# pair-journal.sh — log pair session events with timestamps.
# Survives agent compaction; re-read at session start to restore context.
# Usage:
#   pair-journal.sh start "Implement payment retry logic"
#   pair-journal.sh switch "driver=claude navigator=human"
#   pair-journal.sh note "Decided to use exponential backoff"
#   pair-journal.sh end
set -euo pipefail

JOURNAL="${PAIR_JOURNAL:-.pair-journal.md}"
EVENT="${1:?event required: start|switch|note|end}"
shift || true
MSG="${*:-}"
TS=$(date -u +%FT%TZ)

case "$EVENT" in
  start)
    echo "" >> "$JOURNAL"
    echo "## Session $(date -u +%F)" >> "$JOURNAL"
    echo "- $TS start goal=\"$MSG\"" >> "$JOURNAL"
    ;;
  switch|note)
    echo "- $TS $EVENT $MSG" >> "$JOURNAL"
    ;;
  end)
    echo "- $TS end" >> "$JOURNAL"
    git add "$JOURNAL" && git commit -m "chore: pair session $(date +%F)" || true
    ;;
  *)
    echo "Unknown event: $EVENT" >&2; exit 1
    ;;
esac
