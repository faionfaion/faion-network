#!/usr/bin/env bash
# role-overlap.sh — emit per-author file-area distribution from git history.
# Usage: ./role-overlap.sh <since> <repo-root>
# Example: ./role-overlap.sh 90.days .
# Output: TSV with columns: commits, author, area
# Interpretation: author touching >=3 distinct top-level areas = Venn-overlap territory;
#                 author at 1 area = specialist. Feed to role-audit prompt.
set -euo pipefail
since="${1:-90.days}"
root="${2:-.}"
cd "$root"
git log --since="$since" --name-only --pretty=format:'AUTHOR=%aN' \
  | awk '
    /^AUTHOR=/ { author=substr($0,8); next }
    NF {
      n=split($0,p,"/"); area=(n>1?p[1]:"root")
      key=author"\t"area; count[key]++
    }
    END { for (k in count) print count[k]"\t"k }
  ' \
  | sort -nr \
  | awk -F'\t' 'BEGIN{print "commits\tauthor\tarea"} {print $1"\t"$3"\t"$4}'
