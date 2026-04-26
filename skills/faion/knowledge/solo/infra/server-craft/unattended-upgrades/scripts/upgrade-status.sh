#!/usr/bin/env bash
# upgrade-status.sh — Dashboard: config state, pending updates, recent log, timer schedule, blacklist
set -euo pipefail

echo "=============================="
echo "  Upgrade Status Dashboard"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- Auto-Upgrade Config ---"
printf "Enabled:     "
grep -q 'Unattended-Upgrade "1"' /etc/apt/apt.conf.d/20auto-upgrades 2>/dev/null && echo "Yes" || echo "No"
printf "Auto-Reboot: "
grep -oP 'Automatic-Reboot "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not set"
printf "Reboot Time: "
grep -oP 'Automatic-Reboot-Time "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not set"

echo ""
echo "--- Reboot Status ---"
if [ -f /var/run/reboot-required ]; then
    echo "REBOOT REQUIRED"
    cat /var/run/reboot-required.pkgs 2>/dev/null || true
else
    echo "No reboot needed"
fi

echo ""
echo "--- Pending Updates ---"
apt list --upgradable 2>/dev/null | tail -n +2 | head -15
pending=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
echo "Total: $pending packages"

echo ""
echo "--- Recent Upgrade Log ---"
sudo tail -20 /var/log/unattended-upgrades/unattended-upgrades.log 2>/dev/null || echo "(no log)"

echo ""
echo "--- Timer Schedule ---"
systemctl list-timers apt-daily apt-daily-upgrade --no-pager 2>/dev/null | head -5

echo ""
echo "--- Blacklisted Packages ---"
grep -A30 "Package-Blacklist" /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null | grep '^\s*"' | tr -d '";' | awk '{print "  " $1}' || echo "  (none)"
