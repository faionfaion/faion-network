#!/usr/bin/env bash
# check-reboot-required.sh — Report reboot-required status, packages needing it, auto-reboot config
set -euo pipefail

if [ -f /var/run/reboot-required ]; then
    echo "REBOOT REQUIRED on $(hostname)"
    echo ""
    echo "Packages requiring reboot:"
    cat /var/run/reboot-required.pkgs 2>/dev/null || echo "  (list not available)"
    echo ""
    echo "Uptime: $(uptime -p)"
    echo ""
    auto_reboot=$(grep -oP 'Automatic-Reboot "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not configured")
    reboot_time=$(grep -oP 'Automatic-Reboot-Time "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not set")
    echo "Auto-reboot: $auto_reboot"
    echo "Reboot time: $reboot_time"
    exit 1
else
    echo "No reboot needed on $(hostname)"
    last_upgrade=$(stat -c %y /var/log/unattended-upgrades/unattended-upgrades.log 2>/dev/null | cut -d. -f1 || echo "unknown")
    echo "Last upgrade log: $last_upgrade"
    exit 0
fi
