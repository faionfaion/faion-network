#!/usr/bin/env bash
# swap-create.sh — Idempotent swap file creation and fstab persistence
# Usage: sudo bash swap-create.sh [size]
#   size: e.g. 4G (default), 8G, 2G
set -euo pipefail

SIZE="${1:-4G}"
SWAPFILE="/swapfile"

# Already configured?
if swapon --show | grep -q "$SWAPFILE"; then
    echo "[OK] Swap already active: $(swapon --show | grep "$SWAPFILE")"
    exit 0
fi

if [[ -f "$SWAPFILE" ]]; then
    echo "[INFO] $SWAPFILE exists but is not active; re-enabling..."
    chmod 600 "$SWAPFILE"
    mkswap "$SWAPFILE"
    swapon "$SWAPFILE"
else
    echo "[CREATE] Allocating $SIZE swap at $SWAPFILE..."
    fallocate -l "$SIZE" "$SWAPFILE"
    chmod 600 "$SWAPFILE"
    mkswap "$SWAPFILE"
    swapon "$SWAPFILE"
fi

# fstab persistence (idempotent)
if ! grep -q "$SWAPFILE" /etc/fstab; then
    echo "$SWAPFILE none swap sw 0 0" >> /etc/fstab
    echo "[OK] Added $SWAPFILE to /etc/fstab"
fi

# Verify fstab syntax (broken entry can prevent boot)
findmnt --verify && echo "[OK] fstab syntax valid" || { echo "[ERROR] fstab invalid — fix before reboot!"; exit 1; }

echo "[DONE] Swap:"
swapon --show
free -h | grep Swap
