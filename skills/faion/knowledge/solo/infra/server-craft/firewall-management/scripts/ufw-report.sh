#!/usr/bin/env bash
# ufw-report.sh — Status report: rules, listening ports, Docker mappings, exposed 0.0.0.0 ports, recent blocks
set -euo pipefail

echo "=============================="
echo "  Firewall Status Report"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- UFW Status ---"
sudo ufw status verbose

echo ""
echo "--- Rules (Numbered) ---"
sudo ufw status numbered

echo ""
echo "--- Listening Ports ---"
sudo ss -tlnp | column -t

echo ""
echo "--- Docker Port Mappings ---"
if command -v docker &>/dev/null; then
    docker ps --format "table {{.Names}}\t{{.Ports}}" 2>/dev/null || echo "(Docker not running)"
else
    echo "(Docker not installed)"
fi

echo ""
echo "--- Exposed to 0.0.0.0 (potential UFW bypass) ---"
echo "These ports bypass UFW (Docker or direct bindings):"
sudo ss -tlnp | grep '0\.0\.0\.0' | awk '{print $4, $6}' | grep -v ':80\|:443\|:22' | column -t || echo "(none besides web/ssh)"

echo ""
echo "--- Recent Blocks (last hour) ---"
count=$(sudo journalctl -k --since "1 hour ago" --no-pager 2>/dev/null | grep -c "UFW BLOCK" || echo "0")
echo "$count blocked connections in last hour"

echo ""
echo "--- Top Blocked IPs (last 24h) ---"
sudo journalctl -k --since "24 hours ago" --no-pager 2>/dev/null | \
    grep "UFW BLOCK" | \
    grep -oP 'SRC=\K[^ ]+' | \
    sort | uniq -c | sort -rn | head -10 || echo "(no blocks logged)"
