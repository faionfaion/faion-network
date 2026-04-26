#!/usr/bin/env bash
# headless-guards.sh — apply the four guards for Claude Code, Codex, Aider, opencode.
#
# Usage:
#   ./headless-guards.sh <claude|codex|aider|opencode> "<task>" [allowlist]
#
# Each branch sets: print/headless flag, allowlist (where supported),
# max-turns (or wall-clock timeout when no native cap), and closes stdin.

set -euo pipefail

TOOL="${1:?tool name required}"
TASK="${2:?task required}"
ALLOWED="${3:-Read,Edit,Bash(pytest:*)}"
MAX_TURNS="${MAX_TURNS:-20}"
WALL="${WALL:-600}"

case "$TOOL" in
  claude)
    timeout "$WALL" claude -p "$TASK" \
      --output-format stream-json --verbose \
      --allowedTools "$ALLOWED" \
      --max-turns "$MAX_TURNS" \
      < /dev/null
    ;;
  codex)
    timeout "$WALL" codex exec --sandbox workspace-write "$TASK" \
      < /dev/null
    ;;
  aider)
    timeout "$WALL" aider --yes --no-auto-test \
      --max-chat-history-tokens 8000 \
      --message "$TASK" \
      < /dev/null
    ;;
  opencode)
    timeout "$WALL" opencode --headless --max-turns "$MAX_TURNS" "$TASK" \
      < /dev/null
    ;;
  *)
    echo "unknown tool: $TOOL" >&2
    exit 2
    ;;
esac
