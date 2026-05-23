#!/usr/bin/env bash
# figma-elements.sh — extract element names from a Figma file frame for agent critique input
# Requires: curl, jq
# Usage: FIGMA_TOKEN=<token> bash figma-elements.sh <file-key> <node-id>
# Example: FIGMA_TOKEN=xxx bash figma-elements.sh abc123 12:34
FIGMA_TOKEN="${FIGMA_TOKEN:?Set FIGMA_TOKEN env var (read-only token from figma.com/settings)}"
FILE_KEY="${1:?Usage: $0 <file-key> <node-id>}"
NODE_ID="${2:?}"

curl -s \
  -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/${FILE_KEY}/nodes?ids=${NODE_ID}" \
  | jq '
    [.nodes[].document
     | .. | objects
     | select(.type != null and .name != null)
     | {name: .name, type: .type, visible: (.visible // true)}]
    | unique_by(.name)
    | sort_by(.type)
  '
