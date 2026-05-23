#!/usr/bin/env bash
# purpose: Stub empty TASK_*.md files for a wave under a feature directory.
# consumes: feature directory path + list of task ids (e.g., 001 002 003)
# produces: one TASK_<id>.md stub per id under <feature_dir>/todo/
# depends-on: bash + filesystem; no LLM tokens
# token-budget-impact: zero — shell script
#
# create-tasks.sh — create empty TASK_*.md stubs for a wave
# Usage: create-tasks.sh FEATURE_DIR TASK_IDS...
# Example: create-tasks.sh .aidocs/features/in-progress/user-auth 001 002 003

FEATURE_DIR="${1:?Usage: create-tasks.sh feature-dir task-id [task-id ...]}"
shift

mkdir -p "$FEATURE_DIR/todo"

for id in "$@"; do
  FILE="$FEATURE_DIR/todo/TASK_${id}.md"
  if [ -f "$FILE" ]; then
    echo "SKIP $FILE (already exists)"
    continue
  fi
  cat > "$FILE" << EOF
# TASK_${id}: {Title in Imperative Voice}

**Phase:** {N}
**Wave:** {N}

**Description:**
{2-3 sentences: what needs to be done}

**Traces to:**
- AD-{N}: {architectural decision text}
- FR-{N}: {requirement text}

**Depends on:** None

**Blocks:** {TASK_NNN or "None"}

**Complexity:** simple | normal | complex
**Context Estimate:** ~{X}k tokens

**Acceptance Criteria:**
- [ ] {Specific observable outcome}
- [ ] {Another specific criterion}

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | \`{path}\` | {purpose} |

**Technical Notes:**
{Fill after Wave N-1 execution}

**Tests:**
- [ ] Unit: {description}
- [ ] Integration: {description}
EOF
  echo "Created $FILE"
done
