#!/usr/bin/env bash
# purpose: canonical claude -p headless invocation with four required guards
# consumes: task prompt, allowed-tools list, max_turns
# produces: stream-json event stream on stdout, parseable by orchestrator
# depends-on: content/01-core-rules.xml; content/02-invocation-shape.xml
# token-budget-impact: governed by --max-turns; per-turn caps via Claude Code defaults
# run-headless.sh — canonical headless `claude -p` wrapper.
#
# Usage:
#   ./run-headless.sh "<task prompt>" [allowlist] [max_turns]
#
# Defaults:
#   allowlist  = "Read,Edit,Bash(pytest:*),Bash(git:status)"
#   max_turns  = 20
#
# Stdout: stream-json events, one per line.
# Exit:   non-zero if claude returns non-zero or wall-clock timeout fires.

set -euo pipefail

TASK="${1:?task prompt required}"
ALLOWED="${2:-Read,Edit,Bash(pytest:*),Bash(git:status)}"
MAX_TURNS="${3:-20}"
WALL_TIMEOUT="${WALL_TIMEOUT:-600}"

exec timeout "$WALL_TIMEOUT" \
  claude -p "$TASK" \
    --output-format stream-json --verbose \
    --allowedTools "$ALLOWED" \
    --max-turns "$MAX_TURNS" \
    < /dev/null
