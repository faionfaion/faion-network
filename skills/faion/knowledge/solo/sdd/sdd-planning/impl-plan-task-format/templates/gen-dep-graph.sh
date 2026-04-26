#!/usr/bin/env bash
# gen-dep-graph.sh — generate Graphviz DOT dependency graph from a feature's TASK files
# Usage: gen-dep-graph.sh FEATURE_DIR
# Output: DOT format suitable for `dot -Tpng -o graph.png`
# Example: gen-dep-graph.sh .aidocs/features/in-progress/user-auth | dot -Tpng -o deps.png

DIR=${1:?Usage: gen-dep-graph.sh feature-dir}

echo "digraph tasks {"
echo "  rankdir=LR;"
echo "  node [shape=box];"

for f in "$DIR"/todo/*.md "$DIR"/in-progress/*.md "$DIR"/done/*.md; do
  [ -f "$f" ] || continue
  TASK=$(grep -oP 'TASK[-_]\d+' "$f" | head -1 | tr '_' '-')
  [ -z "$TASK" ] && continue
  DEPS=$(grep "Depends on:" "$f" | grep -oP 'TASK[-_]\d+' | tr '_' '-')
  for dep in $DEPS; do
    echo "  \"$dep\" -> \"$TASK\";"
  done
done

echo "}"
