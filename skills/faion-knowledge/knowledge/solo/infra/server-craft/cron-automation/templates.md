# Cron Automation Templates

## Cron Job Script Template

```bash
#!/bin/bash
# script-name.sh
# Description: What this script does
# Schedule: 0 3 * * * (daily at 3 AM)
# Author: NERO platform automation

set -euo pipefail

# === Configuration ===
SCRIPT_NAME="$(basename "$0" .sh)"
LOG_FILE="/var/log/nero-${SCRIPT_NAME}.log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"

# === Logging ===
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$SCRIPT_NAME] $1" >> "$LOG_FILE"
}

# === Locking (prevent overlapping runs) ===
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "ERROR: Another instance is already running, exiting"
    exit 1
fi

# === Error handling ===
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log "ERROR: Failed with exit code $exit_code"
        # Uncomment for Telegram alerts:
        # /usr/local/bin/notify-telegram.sh "CRON FAIL: $SCRIPT_NAME (exit $exit_code)" 2>/dev/null || true
    fi
}
trap cleanup EXIT

# === Load environment ===
if [ -f "$HOME/workspace/.env" ]; then
    set -a
    source "$HOME/workspace/.env"
    set +a
fi

# === Main logic ===
log "Starting..."

# Your code here
# ...

log "Completed successfully"
```

## FLOW Hourly Monitor

```bash
#!/bin/bash
# flow-hourly.sh
# FLOW hourly health check - alerts only on problems
# Schedule: 0 * * * *

set -euo pipefail

SCRIPT_NAME="flow-hourly"
LOG_FILE="/var/log/nero-flow.log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') [$SCRIPT_NAME] $1" >> "$LOG_FILE"; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "Skipping (locked)"; exit 0; }

source "$HOME/workspace/.env" 2>/dev/null || true

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

# Check API health
if ! curl -sf --max-time 10 http://127.0.0.1:8100/health > /dev/null 2>&1; then
    add_issue "API health check failed"
fi

# Check disk space
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
[ "$DISK_PCT" -gt 90 ] && add_issue "Disk: ${DISK_PCT}%"

# Check memory
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
[ "$MEM_AVAIL" -lt 500 ] && add_issue "Low memory: ${MEM_AVAIL}MB available"

# Check OOM events
OOM=$(journalctl -k --since "1 hour ago" --no-pager 2>/dev/null | grep -c "Out of memory" || true)
[ "$OOM" -gt 0 ] && add_issue "OOM killer: ${OOM}x in last hour"

# Report
if [ -n "$ISSUES" ]; then
    MSG="FLOW ALERT $(hostname) $(date '+%H:%M'):\n$ISSUES"
    echo -e "$MSG" | /usr/local/bin/notify-telegram.sh 2>/dev/null || true
    log "ALERT: $(echo -e "$ISSUES" | tr '\n' ' ')"
else
    log "All OK"
fi
```

## FLOW Daily Report

```bash
#!/bin/bash
# flow-send-daily.sh
# FLOW daily status report sent to Telegram
# Schedule: 0 22 * * *

set -euo pipefail

source "$HOME/workspace/.env" 2>/dev/null || true

R=""
a() { R="${R}$1\n"; }

a "*Daily Report $(date '+%Y-%m-%d %H:%M')*"
a "Host: $(hostname) | Up: $(uptime -p | sed 's/up //')"
a ""

# Services
a "*Services:*"
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    st=$(systemctl --user is-active "$svc" 2>/dev/null || echo "?")
    mem=$(systemctl --user show "$svc" -p MemoryCurrent --value 2>/dev/null || echo "0")
    mem_mb=$((mem / 1048576))
    a "  $svc: $st (${mem_mb}MB)"
done
a ""

# Docker
a "*Docker:*"
for ct in nero-postgres nero-redis nero-rabbitmq nero-flower; do
    st=$(docker inspect -f '{{.State.Status}}' "$ct" 2>/dev/null || echo "?")
    a "  $ct: $st"
done
a ""

# Resources
a "*Resources:*"
a "  CPU: $(awk '{printf "%.1f", $1}' /proc/loadavg) / $(nproc) cores"
a "  RAM: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
a "  Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
a "  Swap: $(free -h | awk '/Swap:/ {print $3 "/" $2}')"
a ""

# Errors (24h)
ERR_COUNT=$(journalctl --user -u 'nero-*' --since "24 hours ago" -p err --no-pager 2>/dev/null | wc -l)
a "*Errors (24h):* $ERR_COUNT"

# Backup
LAST_BK=$(ls -td /home/nero/backups/20* 2>/dev/null | head -1)
if [ -n "$LAST_BK" ]; then
    AGE=$((( $(date +%s) - $(stat -c %Y "$LAST_BK") ) / 3600))
    SIZE=$(du -sh "$LAST_BK" | cut -f1)
    a "*Backup:* $(basename "$LAST_BK") ($SIZE, ${AGE}h ago)"
else
    a "*Backup:* NONE"
fi

echo -e "$R" | /usr/local/bin/notify-telegram.sh
echo "$(date '+%Y-%m-%d %H:%M:%S') [flow-daily] Report sent" >> /var/log/nero-flow.log
```

## FLOW Weekly Report

```bash
#!/bin/bash
# flow-send-weekly.sh
# FLOW weekly trends report
# Schedule: 0 7 * * 1

set -euo pipefail

source "$HOME/workspace/.env" 2>/dev/null || true

R=""
a() { R="${R}$1\n"; }

a "*Weekly Report $(date '+%Y-%m-%d')*"
a ""

# Service restarts this week
a "*Service Restarts (7d):*"
for svc in nero-core nero-channel-web nero-channel-tg; do
    count=$(journalctl --user -u "$svc" --since "7 days ago" --no-pager 2>/dev/null | grep -c "Started" || true)
    a "  $svc: $count restarts"
done
a ""

# Error trends
a "*Errors by Day:*"
for i in 6 5 4 3 2 1 0; do
    day=$(date -d "$i days ago" +%Y-%m-%d)
    count=$(journalctl --user -u 'nero-*' --since "$day 00:00:00" --until "$day 23:59:59" -p err --no-pager 2>/dev/null | wc -l)
    bar=$(printf '%0.s|' $(seq 1 $((count > 0 ? count : 0)) 2>/dev/null) 2>/dev/null || true)
    a "  $day: $count ${bar:0:30}"
done
a ""

# Disk usage trend
a "*Disk:* $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
a "*Docker:* $(docker system df --format '{{.Type}}: {{.Size}}' 2>/dev/null | tr '\n' ', ')"

echo -e "$R" | /usr/local/bin/notify-telegram.sh
echo "$(date '+%Y-%m-%d %H:%M:%S') [flow-weekly] Report sent" >> /var/log/nero-flow.log
```

## Startup Heartbeat

```bash
#!/bin/bash
# startup-heartbeat.sh
# Notify on server boot
# Schedule: @reboot sleep 5 && /path/to/startup-heartbeat.sh

set -euo pipefail

# Wait for services to stabilize
sleep 30

source "$HOME/workspace/.env" 2>/dev/null || true

# Collect status
SVC_UP=0 SVC_DOWN=0 DOCKER_UP=0

for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    if systemctl --user is-active --quiet "$svc" 2>/dev/null; then
        SVC_UP=$((SVC_UP + 1))
    else
        SVC_DOWN=$((SVC_DOWN + 1))
    fi
done

for ct in nero-postgres nero-redis nero-rabbitmq; do
    docker inspect -f '{{.State.Running}}' "$ct" 2>/dev/null | grep -q true && DOCKER_UP=$((DOCKER_UP + 1))
done

MSG="*Server Booted: $(hostname)*
$(date '+%Y-%m-%d %H:%M:%S')
Services: ${SVC_UP} up, ${SVC_DOWN} down
Docker: ${DOCKER_UP}/3 containers
Uptime: $(uptime -p)"

echo "$MSG" | /usr/local/bin/notify-telegram.sh 2>/dev/null || true
echo "$(date) Heartbeat sent" >> /var/log/nero-startup.log
```

## Complete Crontab Template

```cron
# NERO Platform Crontab
# Last updated: 2026-03-21
# Edit: crontab -e | List: crontab -l | Backup: crontab -l > crontab.txt

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/nero/.local/bin
MAILTO=""

# === Config Sync ===
*/15 * * * * /home/nero/workspace/scripts/sync-claude-md.sh >/dev/null 2>&1

# === FLOW Monitoring ===
# Hourly health check (alert only on problems)
0 * * * * /home/nero/workspace/scripts/flow-hourly.sh >> /var/log/nero-flow.log 2>&1

# Checkpoint summaries (5min after hourly to avoid race)
5 6,9,12,15,18,21 * * * /home/nero/workspace/scripts/flow-summarize.sh >> /var/log/nero-flow.log 2>&1

# Daily report (22:00)
0 22 * * * /home/nero/workspace/scripts/flow-send-daily.sh >> /var/log/nero-flow.log 2>&1

# Weekly report (Monday 7:00)
0 7 * * 1 /home/nero/workspace/scripts/flow-send-weekly.sh >> /var/log/nero-flow.log 2>&1

# Monthly report (1st of month 7:15)
15 7 1 * * /home/nero/workspace/scripts/flow-send-monthly.sh >> /var/log/nero-flow.log 2>&1

# Quarterly report (Jan/Apr/Jul/Oct 1st 7:20)
20 7 1 1,4,7,10 * /home/nero/workspace/scripts/flow-send-quarterly.sh >> /var/log/nero-flow.log 2>&1

# Annual report (Jan 1st 7:25)
25 7 1 1 * /home/nero/workspace/scripts/flow-send-annual.sh >> /var/log/nero-flow.log 2>&1

# === Content & Info ===
# AI News (daily 8:05)
5 8 * * * /home/nero/workspace/scripts/morning-ai-news.sh >> /var/log/nero-news.log 2>&1

# === Backup ===
# Daily database backup (3:00)
0 3 * * * /home/nero/workspace/scripts/backup.sh >> /var/log/nero-backup.log 2>&1

# Weekly restic integrity check (Sunday 5:00)
0 5 * * 0 /home/nero/workspace/scripts/restic-check.sh >> /var/log/nero-backup.log 2>&1

# === Maintenance ===
# Weekly Docker cleanup (Sunday 4:00)
0 4 * * 0 docker system prune -f >> /var/log/nero-maintenance.log 2>&1

# Weekly upstream check (Sunday 3:00)
0 3 * * 0 /home/nero/workspace/scripts/check-upstream.sh >> /var/log/nero-upstream.log 2>&1

# === Startup ===
@reboot sleep 5 && /home/nero/workspace/scripts/startup-heartbeat.sh >> /var/log/nero-startup.log 2>&1
```

## Cron Debugging Script

```bash
#!/bin/bash
# debug-cron.sh
# Simulate cron environment for debugging

echo "=== Cron Environment Simulation ==="
echo ""
echo "Running: $1"
echo "With minimal PATH (simulating cron)..."
echo ""

# Simulate cron's minimal environment
env -i \
    HOME="$HOME" \
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    SHELL="/bin/bash" \
    USER="$USER" \
    LOGNAME="$USER" \
    bash "${1:?Usage: $0 <script-path>}"

echo ""
echo "Exit code: $?"
```
