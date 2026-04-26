#!/bin/bash
# flow-daily.sh
# FLOW-style daily status report sent to Telegram unconditionally.
#
# Cron: 0 22 * * * /home/nero/workspace/scripts/flow-daily.sh >> /var/log/nero-flow.log 2>&1

set -euo pipefail

REPORT=""
add() { REPORT="${REPORT}$1\n"; }

add "*Daily Report: $(date '+%Y-%m-%d %H:%M')*"
add "Host: $(hostname)"
add ""

# Uptime
add "*Uptime:* $(uptime -p)"
add ""

# Service status with memory
add "*Services:*"
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    STATUS=$(systemctl --user is-active "$svc" 2>/dev/null || echo "unknown")
    MEM_BYTES=$(systemctl --user show "$svc" -p MemoryCurrent --value 2>/dev/null || echo "0")
    MEM_MB=$((MEM_BYTES / 1048576))
    add "  ${svc}: ${STATUS} (${MEM_MB}MB)"
done
add ""

# Docker containers
add "*Docker:*"
while IFS= read -r line; do add "  $line"; done < <(docker ps --format "{{.Names}}: {{.Status}}" 2>/dev/null)
add ""

# System resources
add "*Resources:*"
add "  CPU: $(awk '{print $1}' /proc/loadavg) load ($(nproc) cores)"
add "  RAM: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
add "  Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
add "  Swap: $(free -h | awk '/Swap:/ {print $3 "/" $2}')"
add ""

# Error count in last 24h
ERROR_COUNT=$(journalctl --user -u 'nero-*' --since "24 hours ago" -p err --no-pager 2>/dev/null | wc -l)
add "*Errors (24h):* ${ERROR_COUNT}"

# Backup status
LAST_BACKUP=$(ls -td /home/nero/backups/20* 2>/dev/null | head -1 || true)
if [ -n "$LAST_BACKUP" ]; then
    AGE_H=$(( ($(date +%s) - $(stat -c %Y "$LAST_BACKUP")) / 3600 ))
    SIZE=$(du -sh "$LAST_BACKUP" | cut -f1)
    add "*Backup:* $(basename "$LAST_BACKUP") (${SIZE}, ${AGE_H}h ago)"
else
    add "*Backup:* NONE FOUND"
fi

echo -e "$REPORT" | /usr/local/bin/notify-telegram.sh
echo "$(date) Daily report sent"
