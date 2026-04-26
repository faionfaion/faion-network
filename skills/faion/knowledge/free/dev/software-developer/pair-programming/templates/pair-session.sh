#!/usr/bin/env bash
# scripts/pair-session.sh — start a logged pair session with terminal transcript.
# The transcript can be fed to the AI navigator as prior context on session resume.
set -euo pipefail

session_dir="$HOME/.pair-sessions/$(date +%Y-%m-%d_%H%M)"
mkdir -p "$session_dir"
echo "Session: $session_dir"
echo "To resume: cat $session_dir/typescript | claude --session"
# script(1) records all terminal I/O to a file.
exec script -q "$session_dir/typescript"
