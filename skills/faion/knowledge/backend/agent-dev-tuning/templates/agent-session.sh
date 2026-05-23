#!/usr/bin/env bash
# agent-session.sh — Set up tmux session: work + logs + monitor windows
# Usage: bash agent-session.sh [session-name] [workdir]
set -euo pipefail

SESSION="${1:-work}"
WORKDIR="${2:-$HOME/workspace}"

# Ensure linger is enabled (survives SSH disconnect)
if ! loginctl show-user "$(whoami)" 2>/dev/null | grep -q "Linger=yes"; then
    echo "[INFO] Enabling linger for $(whoami)..."
    loginctl enable-linger "$(whoami)" || echo "[WARN] Could not enable linger (run as root once)"
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "[INFO] Session '$SESSION' already exists — attaching"
    tmux attach -t "$SESSION"
    exit 0
fi

echo "[CREATE] tmux session: $SESSION"
tmux new-session -d -s "$SESSION" -n "claude" -c "$WORKDIR"

# Logs window
tmux new-window -t "$SESSION" -n "logs" -c "$WORKDIR"
tmux send-keys -t "${SESSION}:logs" "journalctl --user -f" Enter

# Monitor window
tmux new-window -t "${SESSION}" -n "monitor" -c "$WORKDIR"
tmux send-keys -t "${SESSION}:monitor" "watch -n5 'free -h && echo && systemctl --user list-units --state=active --no-legend'" Enter

# Focus back to claude window
tmux select-window -t "${SESSION}:claude"

echo "[OK] Attaching to session '$SESSION'"
tmux attach -t "$SESSION"
