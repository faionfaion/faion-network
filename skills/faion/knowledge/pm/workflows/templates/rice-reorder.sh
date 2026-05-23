#!/usr/bin/env bash
# purpose: Rank backlog items by RICE score and rewrite sorted INDEX.md
# consumes: .aidocs/features/backlog/*/spec.md (frontmatter RICE)
# produces: .aidocs/features/backlog/INDEX.md (sorted)
# depends-on: yq, awk
# token-budget-impact: low
set -euo pipefail
BACKLOG="${1:-.aidocs/features/backlog}"
OUT="${BACKLOG}/INDEX.md"
echo "# Backlog (RICE-sorted)" > "$OUT"
for f in "$BACKLOG"/*/spec.md; do
  r=$(awk '/^reach:/{print $2}' "$f" 2>/dev/null || echo 0)
  i=$(awk '/^impact:/{print $2}' "$f" 2>/dev/null || echo 0)
  c=$(awk '/^confidence:/{print $2}' "$f" 2>/dev/null || echo 0)
  e=$(awk '/^effort:/{print $2}' "$f" 2>/dev/null || echo 1)
  rice=$(awk "BEGIN{printf \"%.2f\", ($r*$i*$c)/$e}" 2>/dev/null || echo 0)
  echo "$rice $f"
done | sort -rn | awk '{print "- ["$2"]("$2")  rice="$1}' >> "$OUT"
echo "wrote: $OUT"
