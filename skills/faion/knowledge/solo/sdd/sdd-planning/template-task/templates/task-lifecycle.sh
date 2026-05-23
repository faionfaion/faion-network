#!/usr/bin/env bash
# purpose: Move a task file between todo / in-progress / done dirs, validating required sections.
# consumes: a TASK_*.md file authored from templates/task.md
# produces: a moved task file in the target lifecycle directory
# depends-on: filesystem layout .aidocs/features/<feature>/{todo,in-progress,done}/
# token-budget-impact: zero — shell script, no LLM tokens
#
# task-lifecycle.sh
#
# Move a task file through its lifecycle states.
# Verifies required section headers before allowing state transition.
#
# Usage:
#   bash task-lifecycle.sh TASK_FILE TARGET_STATE
#
# TARGET_STATE: in-progress | done
#
# Exit codes:
#   0 — task moved successfully
#   1 — validation failed (task not moved)

set -euo pipefail

TASK_FILE="${1:?usage: task-lifecycle.sh TASK_FILE TARGET_STATE}"
TARGET_STATE="${2:?usage: task-lifecycle.sh TASK_FILE TARGET_STATE}"

if [ ! -f "$TASK_FILE" ]; then
    echo "ERROR: $TASK_FILE not found" >&2
    exit 1
fi

if [ "$TARGET_STATE" != "in-progress" ] && [ "$TARGET_STATE" != "done" ]; then
    echo "ERROR: TARGET_STATE must be 'in-progress' or 'done'" >&2
    exit 1
fi

# Validate required sections for 'done' state
if [ "$TARGET_STATE" = "done" ]; then
    if ! grep -q "## Summary" "$TASK_FILE"; then
        echo "BLOCKED: '## Summary' section missing — fill executor sections before marking done" >&2
        exit 1
    fi
    if ! grep -q "\- \[x\]" "$TASK_FILE"; then
        echo "BLOCKED: No completed items in Summary — task not done" >&2
        exit 1
    fi
fi

# Determine target directory relative to current task location
TASK_DIR="$(dirname "$TASK_FILE")"
FEATURE_DIR="$(dirname "$TASK_DIR")"
TARGET_DIR="$FEATURE_DIR/$TARGET_STATE"

mkdir -p "$TARGET_DIR"
mv "$TASK_FILE" "$TARGET_DIR/$(basename "$TASK_FILE")"

echo "Moved $(basename "$TASK_FILE") → $TARGET_STATE/"
