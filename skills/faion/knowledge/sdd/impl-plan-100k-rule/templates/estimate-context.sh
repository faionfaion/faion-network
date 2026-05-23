#!/usr/bin/env bash
# estimate-context.sh — sum token estimates for a task's file list
# Usage: estimate-context.sh file1 file2 file3 ...
# Flags any task where total estimate exceeds 100k tokens.
# Note: uses byte count as proxy (1 token ~= 4 bytes). Install ttok for accuracy.

AGENT_PROMPT=8000
PROJECT_CTX=12000
TASK_FILE=3000
BUFFER=15000
TOTAL=0

echo "Fixed overhead:"
echo "  Agent prompt:    ${AGENT_PROMPT} tokens"
echo "  Project context: ${PROJECT_CTX} tokens"
echo "  Task file:       ${TASK_FILE} tokens"
echo "  Buffer:          ${BUFFER} tokens"
echo "  Fixed subtotal:  $((AGENT_PROMPT + PROJECT_CTX + TASK_FILE + BUFFER)) tokens"
echo ""
echo "Variable (files to read):"

for f in "$@"; do
  if [ -f "$f" ]; then
    BYTES=$(wc -c < "$f")
    TOKENS=$((BYTES / 4))
    echo "  $f: ~${TOKENS} tokens"
    TOTAL=$((TOTAL + TOKENS))
  else
    echo "  $f: NOT FOUND (skipped)"
  fi
done

GRAND=$((TOTAL + AGENT_PROMPT + PROJECT_CTX + TASK_FILE + BUFFER))
echo ""
echo "Variable subtotal: ~${TOTAL} tokens"
echo "TOTAL ESTIMATE:    ~${GRAND} tokens"

if [ "$GRAND" -gt 100000 ]; then
  echo ""
  echo "WARNING: estimate ${GRAND} exceeds 100k limit — split this task"
  exit 1
elif [ "$GRAND" -gt 80000 ]; then
  echo ""
  echo "WATCH: estimate ${GRAND} is in 80-100k range — review before assigning"
fi
