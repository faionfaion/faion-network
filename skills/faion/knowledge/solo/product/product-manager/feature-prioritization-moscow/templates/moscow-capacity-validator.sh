#!/usr/bin/env bash
# moscow-validate.sh <items.csv> <capacity_weeks>
# CSV format: name,category,effort_weeks
# Exits 1 if Must+Should sum exceeds 80% of capacity.
# Categories must be exactly: Must, Should, Could, Wont
set -euo pipefail

csv="${1:?Usage: moscow-validate.sh items.csv capacity_weeks}"
cap="${2:?Usage: moscow-validate.sh items.csv capacity_weeks}"

awk -F',' -v cap="$cap" '
  NR==1 { next }
  { totals[$2] += $3 }
  END {
    must   = totals["Must"]   + 0
    should = totals["Should"] + 0
    could  = totals["Could"]  + 0
    ms = must + should

    printf "Must:   %.1fw (%.0f%% of capacity)\n", must,   must/cap*100
    printf "Should: %.1fw (%.0f%% of capacity)\n", should, should/cap*100
    printf "Could:  %.1fw (%.0f%% of capacity)\n", could,  could/cap*100
    printf "Must+Should: %.1fw (%.0f%% of capacity)\n", ms, ms/cap*100

    if (ms/cap > 0.80) {
      printf "FAIL: Must+Should = %.0f%% of capacity (exceeds 80%% limit)\n", ms/cap*100
      exit 1
    } else {
      printf "OK: Must+Should within 80%% limit\n"
    }
  }' "$csv"
