#!/usr/bin/env bash
# render-variants.sh — render all design variants to PNG for review
# Input:  $1 = variants root dir (default: designs/)
#         $2 = output dir (default: .tmp/variants/)
# Output: grid-desktop.png + grid-mobile.png via imagemagick montage
# Requires: npx playwright, imagemagick (montage)
set -euo pipefail

ROOT="${1:-designs}"
OUT="${2:-.tmp/variants}"
mkdir -p "$OUT"

for variant in "$ROOT"/variant-*/; do
  name=$(basename "$variant")
  for size in "1440x900" "375x812"; do
    npx playwright screenshot \
      --viewport-size="$size" \
      --wait-for-timeout=500 \
      "file://$(realpath "$variant/index.html")" \
      "$OUT/${name}-${size}.png"
  done
done

# Stitch grid for review (requires imagemagick)
montage "$OUT"/*-1440x900.png -tile 3x -geometry +5+5 "$OUT/grid-desktop.png"
montage "$OUT"/*-375x812.png  -tile 3x -geometry +5+5 "$OUT/grid-mobile.png"

echo "review: $OUT/grid-desktop.png $OUT/grid-mobile.png"
