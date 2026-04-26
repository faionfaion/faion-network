#!/usr/bin/env bash
# new-adr.sh — create next-numbered ADR from template
# Usage: ./new-adr.sh "short title of decision"
# Output: docs/adr/NNNN-short-title.md

set -euo pipefail

ADR_DIR="${ADR_DIR:-docs/adr}"
TEMPLATE_DIR="$(dirname "$0")"
TEMPLATE="$TEMPLATE_DIR/adr-template.md"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"short title of decision\"" >&2
  exit 1
fi

TITLE="$1"
SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"
DATE="$(date +%Y-%m-%d)"

mkdir -p "$ADR_DIR"

# Find next sequence number
LAST="$(ls "$ADR_DIR"/*.md 2>/dev/null | grep -oP '^\d{4}' | sort -n | tail -1 || echo "0000")"
NEXT="$(printf '%04d' $((10#$LAST + 1)))"

OUTPUT="$ADR_DIR/${NEXT}-${SLUG}.md"

if [[ -f "$OUTPUT" ]]; then
  echo "Error: $OUTPUT already exists" >&2
  exit 1
fi

sed \
  -e "s/NNNN/$NEXT/g" \
  -e "s/\[Short Title — Noun Phrase\]/$TITLE/" \
  -e "s/YYYY-MM-DD/$DATE/" \
  "$TEMPLATE" > "$OUTPUT"

echo "Created: $OUTPUT"
