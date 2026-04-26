#!/usr/bin/env bash
# figma-pages.sh — list all pages and top-level frames in a Figma file
# Input: Figma file key (from URL: figma.com/design/<file-key>/...)
# Requires: FIGMA_TOKEN environment variable with a valid Personal Access Token
# Output: PAGE and FRAME names, indented
# Usage: FIGMA_TOKEN=xxx bash figma-pages.sh <file-key>

FILE_KEY=${1:?Usage: FIGMA_TOKEN=xxx bash figma-pages.sh <file-key>}

curl -s "https://api.figma.com/v1/files/${FILE_KEY}?depth=2" \
  -H "X-Figma-Token: ${FIGMA_TOKEN}" \
  | jq -r '
    .document.children[] |
    "PAGE: \(.name)" ,
    (  .children[]? | "  FRAME: \(.name) [\(.type)]" )
  '
