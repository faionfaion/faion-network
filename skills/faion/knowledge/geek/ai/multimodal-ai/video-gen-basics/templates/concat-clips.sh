#!/bin/bash
# purpose: ffmpeg concat helper — assemble clips.txt entries into a single mp4.
# consumes: clips.txt with one absolute mp4 path per line.
# produces: assembled mp4 at the path given as $1 (default output.mp4).
# depends-on: ffmpeg with concat demuxer support (any modern build).
# token-budget-impact: zero.
# Usage: bash concat-clips.sh output.mp4 [clips.txt]
set -euo pipefail

INPUT_LIST="${2:-clips.txt}"
OUTPUT="${1:-output.mp4}"

if [ ! -f "$INPUT_LIST" ]; then
    echo "Error: $INPUT_LIST not found" >&2
    exit 1
fi

# Build ffmpeg concat list
while IFS= read -r f; do
    echo "file '$f'"
done < "$INPUT_LIST" > /tmp/concat_list.txt

ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt -c copy "$OUTPUT"
rm -f /tmp/concat_list.txt
echo "Written: $OUTPUT"
