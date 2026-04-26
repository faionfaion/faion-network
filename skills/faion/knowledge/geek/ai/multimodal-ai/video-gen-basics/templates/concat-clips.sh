#!/bin/bash
# concat-clips.sh — concatenate clips listed in clips.txt
# Usage: bash concat-clips.sh output.mp4
# clips.txt format: one absolute file path per line
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
