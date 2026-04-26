#!/usr/bin/env bash
# export-frames.sh — export all top-level frames from a Figma page to PNG
# Input: Figma file key, page name (default: "Page 1")
# Requires: FIGMA_TOKEN and FILE_KEY environment variables
# Output: PNG files named after each frame, in current directory
# Usage: FIGMA_TOKEN=xxx FILE_KEY=yyy bash export-frames.sh "Page 1"

PAGE_NAME="${1:-Page 1}"

if [ -z "$FIGMA_TOKEN" ] || [ -z "$FILE_KEY" ]; then
  echo "Error: FIGMA_TOKEN and FILE_KEY environment variables required"
  exit 1
fi

echo "Fetching frames from page: $PAGE_NAME"

curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" \
  | jq -r --arg p "$PAGE_NAME" \
    '.document.children[] | select(.name==$p) | .children[] | "\(.id) \(.name)"' \
  | while read -r id name; do
      url=$(curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
        "https://api.figma.com/v1/images/$FILE_KEY?ids=$id&format=png&scale=2" \
        | jq -r ".images[\"$id\"]")
      safe_name="${name// /_}"
      curl -s "$url" -o "${safe_name}.png"
      echo "Saved: ${safe_name}.png"
    done
