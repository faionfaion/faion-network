#!/usr/bin/env bash
# purpose: Audit a source tree for LLM-friendly architecture compliance (file size, depth, naming).
# consumes: A source directory path + an optional line-limit override (default 300).
# produces: A JSON report listing each violating file with the violated rule.
# depends-on: Standard POSIX shell utilities (find, awk, wc).
# token-budget-impact: zero — local shell run, no LLM calls.
# llm-arch-audit.sh — Audit source files for LLM-friendly architecture compliance.
# Usage: bash llm-arch-audit.sh [src-dir] [line-limit]
# Input:  source directory (default: src), line limit (default: 250)
# Output: files exceeding limit (sorted by size), barrel re-export files

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
echo "=== Barrel re-exports (potential agent navigation traps) ==="
if command -v rg &>/dev/null; then
  rg --glob "*.ts" "^export \* from" "$DIR" -l
else
  grep -rl "^export \* from" "$DIR" --include="*.ts"
fi