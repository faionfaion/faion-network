#!/usr/bin/env bash
# Build QUEUE.txt with absolute paths of methodologies lacking agent-integration.md
set -euo pipefail

REPO_ROOT=/home/nero/workspace/projects/faion-net/faion-network
KNOWLEDGE=$REPO_ROOT/skills/faion/knowledge
RESEARCH_DIR=$REPO_ROOT/skills/faion/.research
QUEUE=$RESEARCH_DIR/QUEUE.txt

: > "$QUEUE"

# Find all methodology dirs (contain README.md) at depth 4 from knowledge/
# Structure: knowledge/<tier>/<group>/<domain>/<methodology>/README.md
while IFS= read -r readme; do
  dir=$(dirname "$readme")
  # Skip if agent-integration.md already exists
  if [ -f "$dir/agent-integration.md" ]; then
    continue
  fi
  # Skip top-level / index dirs that happen to have READMEs but aren't methodologies
  # Methodology dirs sit at depth 4 under knowledge/
  rel=${dir#$KNOWLEDGE/}
  depth=$(awk -F/ '{print NF}' <<< "$rel")
  if [ "$depth" -lt 4 ]; then
    continue
  fi
  echo "$dir" >> "$QUEUE"
done < <(find "$KNOWLEDGE" -mindepth 5 -maxdepth 5 -name README.md)

count=$(wc -l < "$QUEUE")
echo "QUEUE built: $count methodologies"
