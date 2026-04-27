#!/bin/bash
# Generates UI variants from a prompts file using v0 CLI, saves outputs.
# Usage: ./gen-ui.sh prompts.txt [output-dir/]
# Requires: v0 CLI installed (npm i -g v0)

PROMPTS_FILE="$1"
OUT_DIR="${2:-ui-variants}"
mkdir -p "$OUT_DIR"

i=1
while IFS= read -r prompt; do
  echo "Generating variant $i..."
  v0 generate "$prompt" --format react > "$OUT_DIR/variant_$i.tsx" 2>&1
  echo "Saved variant_$i.tsx"
  ((i++))
done < "$PROMPTS_FILE"

echo "Done. $((i-1)) variants generated in $OUT_DIR/"
