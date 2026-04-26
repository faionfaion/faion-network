#!/usr/bin/env bash
# spatial-budget.sh — fail CI if a glTF/USDZ asset exceeds spatial budget
# Usage: MAX_TRIS=50000 MAX_MB=10 ./spatial-budget.sh path/to/asset.glb
# Requires: gltf-pipeline (npm i -g gltf-pipeline), du
set -euo pipefail

ASSET="${1:?path to asset required}"
MAX_TRIS="${MAX_TRIS:-100000}"
MAX_MB="${MAX_MB:-15}"

SIZE_MB=$(du -m "$ASSET" | cut -f1)
TRIS=$(gltf-pipeline -i "$ASSET" --stats 2>/dev/null | awk '/triangles/{print $2}')

[ "$SIZE_MB" -le "$MAX_MB" ] || {
  echo "FAIL size ${SIZE_MB}MB > ${MAX_MB}MB: $ASSET"
  exit 1
}
[ -n "$TRIS" ] && [ "$TRIS" -le "$MAX_TRIS" ] || {
  echo "FAIL tris ${TRIS:-unknown} > ${MAX_TRIS}: $ASSET"
  exit 1
}
echo "OK $ASSET — ${SIZE_MB}MB / ${TRIS} tris"
