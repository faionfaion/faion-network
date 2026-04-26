#!/usr/bin/env bash
# rice-reorder.sh — rank backlog by RICE = (R*I*C)/E, write INDEX.md
# Usage: rice-reorder.sh [backlog-root]
# Reads spec.md frontmatter for: reach, impact, confidence, effort fields.
# Output: INDEX.md in the backlog root, sorted by RICE descending.
set -euo pipefail
ROOT="${1:-.aidocs/features/backlog}"
OUT="$ROOT/INDEX.md"
{
  echo "# Backlog (RICE-sorted)"
  echo
  printf '| Feature | Reach | Impact | Conf | Effort | RICE |\n'
  printf '|---------|------:|------:|----:|------:|----:|\n'
  for spec in "$ROOT"/*/spec.md; do
    feat=$(basename "$(dirname "$spec")")
    R=$(awk -F': ' '/^reach:/{print $2; exit}' "$spec")
    I=$(awk -F': ' '/^impact:/{print $2; exit}' "$spec")
    C=$(awk -F': ' '/^confidence:/{print $2; exit}' "$spec")
    E=$(awk -F': ' '/^effort:/{print $2; exit}' "$spec")
    [ -z "$R" ] || [ -z "$I" ] || [ -z "$C" ] || [ -z "$E" ] && {
      echo "WARN: missing RICE fields in $spec" >&2; continue
    }
    [ "$E" = "0" ] && { echo "WARN: effort=0 in $spec, skipping" >&2; continue; }
    RICE=$(python3 -c "print(round($R*$I*$C/$E,1))")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$feat" "$R" "$I" "$C" "$E" "$RICE"
  done | sort -k6 -nr \
       | awk -F'\t' '{printf "| %s | %s | %s | %s | %s | %s |\n",$1,$2,$3,$4,$5,$6}'
} > "$OUT"
echo "wrote $OUT"
