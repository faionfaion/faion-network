#!/bin/bash
# flow-hourly.sh
# FLOW-style hourly health monitor — silent on success, alerts only on problems.
#
# Cron: 0 * * * * /home/nero/workspace/scripts/flow-hourly.sh >> /var/log/nero-flow.log 2>&1

set -euo pipefail

ISSUES=""
add_issue() { ISSUES="${ISSUES}- $1\n"; }

# Check systemd user services
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat; do
    if ! systemctl --user is-active --quiet "$svc" 2>/dev/null; then
        add_issue "$svc is DOWN"
    fi
done

# Check Docker containers
for ct in nero-postgres nero-redis nero-rabbitmq; do
    if ! docker inspect -f '{{.State.Running}}' "$ct" 2>/dev/null | grep -q true; then
        add_issue "Docker: $ct is DOWN"
    fi
done

# Check API endpoint
if ! curl -sf --max-time 10 http://127.0.0.1:8100/health > /dev/null 2>&1; then
    add_issue "API health check failed"
fi

# Check disk space
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -gt 90 ]; then
    add_issue "Disk usage: ${DISK_PCT}%"
fi

# Check available memory (less than 500MB available)
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
if [ "$MEM_AVAIL" -lt 500 ]; then
    add_issue "Low memory: ${MEM_AVAIL}MB available"
fi

# Check for recent OOM kills
OOM_COUNT=$(journalctl -k --since "1 hour ago" --no-pager 2>/dev/null | grep -c "Out of memory" || true)
if [ "$OOM_COUNT" -gt 0 ]; then
    add_issue "OOM killer triggered ${OOM_COUNT} times in last hour"
fi

# Report: alert only if issues found
if [ -n "$ISSUES" ]; then
    echo -e "FLOW ALERT $(hostname) $(date '+%H:%M'):\n$ISSUES" | \
        /usr/local/bin/notify-telegram.sh
    echo "$(date) ISSUES:$(echo -e "$ISSUES")"
else
    echo "$(date) All OK"
fi
