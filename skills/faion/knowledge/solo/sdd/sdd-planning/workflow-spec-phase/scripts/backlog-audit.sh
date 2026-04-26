#!/usr/bin/env bash
# backlog-audit.sh — Print feature status table across all SDD lifecycle stages.
# Usage: ./backlog-audit.sh [aidocs-dir]
# Default aidocs-dir: .aidocs
# Output: markdown table with spec/design/plan existence per feature per stage
set -euo pipefail

DOCS_DIR="${1:-.aidocs}/features"

if [ ! -d "$DOCS_DIR" ]; then
  echo "Directory not found: $DOCS_DIR"
  echo "Usage: $0 [aidocs-root-dir]"
  exit 1
fi

echo "| Stage | Feature | Spec | Design | Plan |"
echo "|-------|---------|------|--------|------|"

for stage in backlog todo in-progress done; do
  dir="$DOCS_DIR/$stage"
  [ -d "$dir" ] || continue
  for feature in "$dir"/*/; do
    [ -d "$feature" ] || continue
    name=$(basename "$feature")
    spec=$( [ -f "$feature/spec.md" ] && grep -m1 'Status:' "$feature/spec.md" 2>/dev/null | sed 's/.*Status: //' || echo "missing" )
    design=$( [ -f "$feature/design.md" ] && grep -m1 'Status:' "$feature/design.md" 2>/dev/null | sed 's/.*Status: //' || echo "missing" )
    plan=$( [ -f "$feature/implementation-plan.md" ] && grep -m1 'Status:' "$feature/implementation-plan.md" 2>/dev/null | sed 's/.*Status: //' || echo "missing" )
    echo "| $stage | $name | $spec | $design | $plan |"
  done
done
