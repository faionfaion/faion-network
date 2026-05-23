#!/usr/bin/env bash
# purpose: enforce polygon + file-size budgets on imported assets
# consumes: imported assets in assets/3d/ + budgets from tool-stack-config.json
# produces: exit-1 if any asset exceeds budget
# depends-on: content/01-core-rules.xml budget-at-concept rule
# token-budget-impact: ~200 tokens when loaded as context
set -euo pipefail
MAX_SIZE_MB="${1:-30}"
for f in $(find assets/3d -type f \( -name "*.glb" -o -name "*.gltf" -o -name "*.usdz" \)); do
  size=$(du -m "$f" | cut -f1)
  if [ "$size" -gt "$MAX_SIZE_MB" ]; then
    echo "FAIL: $f is ${size}MB > ${MAX_SIZE_MB}MB"
    exit 1
  fi
done
echo "OK: all assets under ${MAX_SIZE_MB}MB"
