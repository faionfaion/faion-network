#!/bin/bash
# purpose: Template fixture for tmux-power-user: tmux-session.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
# tmux-session.sh
# Generic create-or-attach session launcher — safe to call repeatedly.
#
# Usage:
#   tmux-session.sh <session-name> [project-dir]
#   tmux-session.sh nero ~/workspace/projects/nero
#
# If the session already exists, attaches to it.
# If it does not exist, creates it with a standard 3-window layout.

set -euo pipefail

SESSION="${1:-dev}"
DIR="${2:-$(pwd)}"

# Attach if session already exists (idempotent)
if tmux has-session -t "$SESSION" 2>/dev/null; then
    exec tmux attach -t "$SESSION"
fi

# Create new session
tmux new-session -d -s "$SESSION" -c "$DIR"

# Window 1: editor / main work
tmux rename-window -t "$SESSION:1" "edit"

# Window 2: terminal
tmux new-window -t "$SESSION" -n "term" -c "$DIR"

# Window 3: run/logs (split into two panes)
tmux new-window -t "$SESSION" -n "run" -c "$DIR"
tmux split-window -h -t "$SESSION:run" -c "$DIR"

# Focus on window 1
tmux select-window -t "$SESSION:1"

exec tmux attach -t "$SESSION"
