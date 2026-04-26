#!/usr/bin/env bash
# llm-arch-audit.sh — Find files violating LLM-friendly architecture limits.
# Usage: bash llm-arch-audit.sh [src-dir] [line-limit]
# Input:  source directory (default: src), line limit (default: 250)
# Output: files exceeding limit (sorted by size desc), barrel re-export files

DIR=${1:-src}
LIMIT=${2:-250}

echo "=== Files exceeding ${LIMIT} lines in ${DIR} ==="
find "$DIR" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) \
  | while read -r f; do
      lines=$(wc -l < "$f")
      if [ "$lines" -gt "$LIMIT" ]; then
        echo "$lines  $f"
      fi
    done \
  | sort -rn

echo ""
echo "=== Barrel re-exports (agent navigation traps) ==="
if command -v rg &>/dev/null; then
  rg --glob "*.ts" "^export \* from" "$DIR" -l
else
  grep -rl "^export \* from" "$DIR" --include="*.ts"
fi
