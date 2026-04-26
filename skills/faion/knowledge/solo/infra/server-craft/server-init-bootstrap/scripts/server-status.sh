#!/usr/bin/env bash
# server-status.sh — Dashboard: uptime, disk, memory, swap, running services, UFW rules, open ports
set -euo pipefail

echo "=============================="
echo "  Server Status"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- System ---"
echo "Uptime:   $(uptime -p)"
echo "Load:     $(uptime | awk -F'load average: ' '{print $2}')"
echo "Kernel:   $(uname -r)"

echo ""
echo "--- Memory ---"
free -h | grep -v "^$"

echo ""
echo "--- Swap ---"
swapon --show 2>/dev/null || echo "(no swap)"

echo ""
echo "--- Disk ---"
df -h / | tail -1 | awk '{print "Root: " $3 " used / " $2 " total (" $5 " used)"}'
df -h --total 2>/dev/null | tail -1 || true

echo ""
echo "--- Running Services ---"
systemctl list-units --type=service --state=running --no-pager 2>/dev/null | head -20

echo ""
echo "--- UFW Rules ---"
sudo ufw status 2>/dev/null | head -20

echo ""
echo "--- Open Ports ---"
sudo ss -tlnp | column -t
