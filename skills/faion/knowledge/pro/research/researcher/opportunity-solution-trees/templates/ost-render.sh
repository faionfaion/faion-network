#!/usr/bin/env bash
# ost-render.sh — convert ost.yaml to Mermaid diagram and render to SVG
# Requires: yq, jq, mmdc (npm i -g @mermaid-js/mermaid-cli)
# Usage: ./ost-render.sh [ost.yaml] [output.svg]
set -euo pipefail

INPUT="${1:-ost.yaml}"
OUTPUT="${2:-ost.svg}"
MMD="$(mktemp /tmp/ost-XXXX.mmd)"

yq -o=json "$INPUT" | jq -r '
  "graph TD",
  (.outcome | "O[\(.id): \(.metric | gsub(" "; "_"))]"),
  (.opportunities[] | "O --> \(.id)[\(.statement | gsub(" "; "_") | .[0:40])]"),
  (.solutions[] | "\(.parent) --> \(.id)((\(.statement | gsub(" "; "_") | .[0:30])))"),
  (.experiments[] | "\(.parent) --> \(.id)>\(.type)]")
' > "$MMD"

mmdc -i "$MMD" -o "$OUTPUT"
rm -f "$MMD"
echo "Rendered: $OUTPUT"
