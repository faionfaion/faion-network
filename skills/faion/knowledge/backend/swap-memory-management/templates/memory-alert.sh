#!/usr/bin/env bash
# purpose: Template fixture for swap-memory-management: memory-alert.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
# memory-alert.sh — Alert when RAM or swap exceeds threshold
# Usage: bash memory-alert.sh [ram_threshold] [swap_threshold]
#   Defaults: RAM 90%, Swap 50%
# Suitable for cron: */5 * * * * bash ~/workspace/scripts/memory-alert.sh
set -euo pipefail

RAM_THRESHOLD="${1:-90}"
SWAP_THRESHOLD="${2:-50}"

ram_pct=$(free | awk '/^Mem:/{printf "%.0f", $3/$2 * 100}')
swap_total=$(free | awk '/^Swap:/{print $2}')
if [[ "$swap_total" -gt 0 ]]; then
    swap_pct=$(free | awk '/^Swap:/{printf "%.0f", $3/$2 * 100}')
else
    swap_pct=0
fi

alert=false

if [[ "$ram_pct" -gt "$RAM_THRESHOLD" ]]; then
    echo "ALERT: RAM usage at ${ram_pct}% (threshold: ${RAM_THRESHOLD}%)"
    alert=true
fi

if [[ "$swap_pct" -gt "$SWAP_THRESHOLD" ]]; then
    echo "ALERT: Swap usage at ${swap_pct}% (threshold: ${SWAP_THRESHOLD}%)"
    alert=true
fi

if [[ "$alert" == "true" ]]; then
    echo ""
    echo "Top memory consumers:"
    ps aux --sort=-%mem --no-headers | head -8 | awk '{printf "  %-20s %5s%% %s\n", $1, $4, $11}'

    echo ""
    echo "Swap usage by process:"
    for f in /proc/[0-9]*/status; do
        awk '/VmSwap|Name/{printf $2 " " $3}END{print ""}' "$f" 2>/dev/null
    done | sort -k2 -rn | head -5

    # Optionally notify via Telegram (requires tg-send in PATH)
    if command -v tg-send &>/dev/null; then
        tg-send "Memory alert on $(hostname): RAM=${ram_pct}%, Swap=${swap_pct}%"
    fi
    exit 1
fi

echo "OK: RAM=${ram_pct}%, Swap=${swap_pct}%"
