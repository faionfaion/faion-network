#!/bin/bash
# purpose: Pre-existing tmux session-save hook (UserPromptSubmit/SubagentStart).
# consumes: inputs declared in claude-code-hooks/AGENTS.md Prerequisites table
# produces: artefact matching claude-code-hooks/content/02-output-contract.xml
# depends-on: rules in claude-code-hooks/content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when filled
# ~/.claude/hooks/tmux-save.sh
# UserPromptSubmit + SubagentStart hook: save tmux pane content for session continuity.
# Keeps last 10 captures. No-op when not running in tmux.

INPUT=$(cat)  # consume stdin even though we don't use it

if [ -z "${TMUX:-}" ]; then
    echo '{"status":"ok"}'
    exit 0
fi

SAVE_DIR="$HOME/.claude/tmux-captures"
mkdir -p "$SAVE_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CAPTURE_FILE="$SAVE_DIR/capture_${TIMESTAMP}.txt"

tmux capture-pane -t "${TMUX_PANE:-}" -p > "$CAPTURE_FILE" 2>/dev/null

# Retain only the last 10 captures
ls -t "$SAVE_DIR"/capture_*.txt 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null

echo '{"status":"ok"}'
