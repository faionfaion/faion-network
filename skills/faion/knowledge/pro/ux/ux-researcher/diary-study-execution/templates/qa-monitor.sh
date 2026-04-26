#!/usr/bin/env bash
# qa-monitor.sh — Flag low completion and suspected copy-paste entries.
# Input:  $1 = entries.csv (columns: participant_id, date, text, ...)
#         $2 = expected days in study
# Output: LOW: lines for participants below 60% completion
#         DUP: lines for suspected copy-paste (identical text across days)
# Run: bash qa-monitor.sh entries.csv 14

set -euo pipefail

INDEX="${1:?Usage: qa-monitor.sh entries.csv expected_days}"
EXPECTED_DAYS="${2:?Usage: qa-monitor.sh entries.csv expected_days}"

echo "=== Completion Check (threshold: 60%) ==="
awk -F, -v exp="$EXPECTED_DAYS" '
  NR > 1 {
    count[$1]++
  }
  END {
    for (p in count) {
      pct = int((count[p] * 100) / exp)
      if (pct < 60) {
        printf "LOW: participant=%s  entries=%d/%d  completion=%d%%\n",
               p, count[p], exp, pct
      }
    }
  }
' "$INDEX"

echo ""
echo "=== Copy-Paste Detection (identical text across days) ==="
awk -F, '
  NR > 1 {
    key = $1 "|" $3   # participant_id | text
    n[key]++
    if (n[key] == 2) {
      print "DUP: participant=" $1 "  text=" substr($3, 1, 60) "..."
    }
  }
' "$INDEX"
