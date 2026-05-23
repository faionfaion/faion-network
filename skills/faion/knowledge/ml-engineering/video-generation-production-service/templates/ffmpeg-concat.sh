#!/usr/bin/env bash
# purpose: concat N clips into one mp4 + optional watermark
# consumes: clips/*.mp4 list + watermark.png
# produces: code (post-process script)
# depends-on: ffmpeg in PATH
# token-budget-impact: 0
set -euo pipefail

OUT="${1:-out.mp4}"
CLIPS_DIR="${2:-clips}"

# build concat list
> list.txt
for f in "$CLIPS_DIR"/*.mp4; do
  echo "file '$PWD/$f'" >> list.txt
done

# concat
ffmpeg -y -f concat -safe 0 -i list.txt -c copy "$OUT"

# optional watermark
if [ -f watermark.png ]; then
  ffmpeg -y -i "$OUT" -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" -codec:a copy "${OUT%.mp4}_wm.mp4"
fi
