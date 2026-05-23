#!/usr/bin/env bash
# cr_drift.sh — sum schedule/cost impact of approved CRs in a Markdown register.
# Usage: bash cr_drift.sh [CHANGE-REGISTER.md]
# Reads the register table, finds "Approved" rows, sums +Days and +Cost columns.
# Adjust column indices ($6 for days, $7 for cost) to match your register layout.
set -euo pipefail

file="${1:-CHANGE-REGISTER.md}"

if [[ ! -f "$file" ]]; then
    echo "ERROR: $file not found" >&2
    exit 1
fi

awk -F'|' '
    # Match rows where the Decision column (col 8) contains "Approved"
    /Approved/ && NF >= 9 {
        # Extract numeric values from +Days and +Cost columns
        days_raw = $6; cost_raw = $7
        gsub(/[^0-9.]/, "", days_raw)
        gsub(/[^0-9.]/, "", cost_raw)
        if (days_raw != "") days_total += days_raw
        if (cost_raw != "") cost_total += cost_raw
        approved++
    }
    END {
        printf "approved_crs=%d  total_days=%.1f  total_cost_usd=%.0f\n",
            approved, days_total, cost_total
    }
' "$file"
