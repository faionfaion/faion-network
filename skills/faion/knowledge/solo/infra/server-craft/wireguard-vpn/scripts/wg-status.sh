#!/usr/bin/env bash
# wg-status.sh — Show peer handshake age, data transfer, active/stale status
set -euo pipefail

echo "=============================="
echo "  WireGuard Status"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- Interface ---"
sudo wg show

echo ""
echo "--- Peer Handshake Age ---"
now=$(date +%s)
sudo wg show wg0 latest-handshakes 2>/dev/null | while read -r pubkey handshake; do
    if [ "$handshake" -eq 0 ] 2>/dev/null; then
        echo "  $pubkey — NEVER connected"
    else
        age=$(( now - handshake ))
        if [ "$age" -lt 180 ]; then
            status="ACTIVE"
        elif [ "$age" -lt 600 ]; then
            status="RECENT (${age}s ago)"
        else
            status="STALE (${age}s ago)"
        fi
        echo "  $pubkey — $status"
    fi
done

echo ""
echo "--- Data Transfer per Peer ---"
sudo wg show wg0 transfer 2>/dev/null || echo "(no transfer data)"
