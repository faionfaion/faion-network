#!/usr/bin/env bash
# watcher-status.sh — Show watcher log tail, restart counts, last alert timestamps
set -euo pipefail

echo "=============================="
echo "  Watcher Status"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- Watcher Service ---"
systemctl --user status watcher.service --no-pager 2>/dev/null || echo "(watcher not installed)"

echo ""
echo "--- Recent Restarts ---"
journalctl --user -u watcher.service --since "24 hours ago" --no-pager 2>/dev/null | \
    grep -i "restart\|unhealthy\|max restarts" | tail -20 || echo "(no log)"

echo ""
echo "--- Service Restart History (24h) ---"
journalctl --user --since "24 hours ago" --no-pager 2>/dev/null | \
    grep "Started\|Stopped\|Failed" | grep -v "watcher" | tail -20 || echo "(no log)"
