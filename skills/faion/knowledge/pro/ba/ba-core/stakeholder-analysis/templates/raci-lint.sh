#!/usr/bin/env bash
# raci-lint.sh — fail if any RACI row has != 1 Accountable or 0 Responsible.
# Usage: raci-lint.sh path/to/raci.md
set -euo pipefail
file="${1:?path required}"
errors=0
awk '
  /^\| *Activity *\|/ { in_tbl=1; print; next }
  in_tbl && /^\|[- |]+\|$/ { print; next }
  in_tbl && /^\|/ { print; next }
  in_tbl && !/^\|/ { in_tbl=0 }
' "$file" | while IFS= read -r row; do
  [[ "$row" =~ Activity ]] && continue
  [[ "$row" =~ ^\|[-\ |]+\|$ ]] && continue
  cells=$(printf '%s' "$row" | tr '|' '\n' | sed 's/^ *//;s/ *$//')
  a_count=$(printf '%s\n' "$cells" | grep -cxE 'A')
  r_count=$(printf '%s\n' "$cells" | grep -cxE 'R')
  activity=$(printf '%s\n' "$cells" | sed -n '2p')
  if [[ "$a_count" -ne 1 ]]; then
    echo "ERR: '$activity' has $a_count A (must be 1)" >&2
    errors=$((errors+1))
  fi
  if [[ "$r_count" -lt 1 ]]; then
    echo "ERR: '$activity' has 0 R (need >=1)" >&2
    errors=$((errors+1))
  fi
done
exit $(( errors > 0 ? 1 : 0 ))
