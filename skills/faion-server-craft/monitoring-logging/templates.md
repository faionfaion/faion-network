# Monitoring & Logging Templates

## Health Check Script

```bash
#!/bin/bash
# health-check.sh
# Comprehensive health check for VPS platform
# Exit codes: 0 = all OK, 1 = warnings, 2 = errors

set -euo pipefail

ERRORS=0
WARNINGS=0

# --- Output helpers ---
ok()   { echo "OK   $1"; }
warn() { echo "WARN $1"; WARNINGS=$((WARNINGS + 1)); }
fail() { echo "FAIL $1"; ERRORS=$((ERRORS + 1)); }

check_service() {
    local name="$1" cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then ok "$name"; else fail "$name"; fi
}

echo "=== Health Check: $(date '+%Y-%m-%d %H:%M:%S') ==="

# --- Docker containers ---
echo ""
echo "--- Infrastructure ---"
check_service "Docker" "systemctl is-active docker"
check_service "PostgreSQL" "docker exec nero-postgres pg_isready -U nero -q"
check_service "Redis" "docker exec nero-redis redis-cli ping"
check_service "RabbitMQ" "docker exec nero-rabbitmq rabbitmq-diagnostics -q ping"

# --- User services ---
echo ""
echo "--- Services ---"
SERVICES=(nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal)
for svc in "${SERVICES[@]}"; do
    check_service "$svc" "systemctl --user is-active --quiet $svc"
done

# --- Endpoints ---
echo ""
echo "--- Endpoints ---"
check_service "API /health" "curl -sf --max-time 5 http://127.0.0.1:8100/health"
check_service "Web frontend" "curl -sf --max-time 5 http://127.0.0.1:8101/ -o /dev/null"

# --- System resources ---
echo ""
echo "--- Resources ---"

# Disk
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -gt 90 ]; then fail "Disk: ${DISK_PCT}%"
elif [ "$DISK_PCT" -gt 80 ]; then warn "Disk: ${DISK_PCT}%"
else ok "Disk: ${DISK_PCT}%"; fi

# Memory
MEM_PCT=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_PCT" -gt 95 ]; then fail "Memory: ${MEM_PCT}%"
elif [ "$MEM_PCT" -gt 85 ]; then warn "Memory: ${MEM_PCT}%"
else ok "Memory: ${MEM_PCT}%"; fi

# CPU load
LOAD=$(awk '{print $1}' /proc/loadavg)
CPUS=$(nproc)
LOAD_PCT=$(echo "$LOAD $CPUS" | awk '{printf "%.0f", ($1/$2)*100}')
if [ "$LOAD_PCT" -gt 90 ]; then warn "CPU Load: $LOAD (${LOAD_PCT}%)"
else ok "CPU Load: $LOAD (${LOAD_PCT}%)"; fi

# Swap
SWAP_TOTAL=$(free -m | awk '/Swap:/ {print $2}')
SWAP_USED=$(free -m | awk '/Swap:/ {print $3}')
if [ "$SWAP_TOTAL" -gt 0 ] && [ "$SWAP_USED" -gt $((SWAP_TOTAL / 2)) ]; then
    warn "Swap: ${SWAP_USED}M/${SWAP_TOTAL}M used"
else
    ok "Swap: ${SWAP_USED}M/${SWAP_TOTAL}M"
fi

# --- Summary ---
echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "RESULT: $ERRORS errors, $WARNINGS warnings"
    exit 2
elif [ "$WARNINGS" -gt 0 ]; then
    echo "RESULT: $WARNINGS warnings"
    exit 1
else
    echo "RESULT: All systems healthy"
    exit 0
fi
```

## tmux System Dashboard

```bash
#!/bin/bash
# tmux-system.sh
# Create a tmux monitoring dashboard

SESSION="monitor"
tmux kill-session -t "$SESSION" 2>/dev/null

tmux new-session -d -s "$SESSION" -n "dashboard"

# Pane 0: top-left - htop
tmux send-keys "htop --sort-key=PERCENT_MEM" C-m

# Pane 1: top-right - Docker stats
tmux split-window -h -l 60
tmux send-keys "docker stats --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}'" C-m

# Pane 2: bottom-left - service status (auto-refresh)
tmux select-pane -t 0
tmux split-window -v -l 12
tmux send-keys "watch -n 15 'systemctl --user status nero-* --no-pager 2>/dev/null | grep -E \"(nero-|Active|Memory|Tasks)\"'" C-m

# Pane 3: bottom-right - combined error log
tmux select-pane -t 2
tmux split-window -h -l 60
tmux send-keys "journalctl --user -u 'nero-*' -f -p warning --no-hostname -o short-iso" C-m

# Focus on htop pane
tmux select-pane -t 0

tmux attach -t "$SESSION"
```

## journald Configuration

```ini
# /etc/systemd/journald.conf
[Journal]
# Persistent storage (survives reboots)
Storage=persistent

# Maximum total journal size
SystemMaxUse=2G

# Maximum per-file size
SystemMaxFileSize=100M

# Runtime (in-memory before flush) limits
RuntimeMaxUse=500M

# Retention period
MaxRetentionSec=30d

# Compression
Compress=yes

# Rate limiting (prevent log spam)
RateLimitIntervalSec=30s
RateLimitBurst=10000

# Forward to syslog (disable if not needed)
ForwardToSyslog=no
```

## logrotate Configuration

```
# /etc/logrotate.d/nero-platform
# Rotate application log files

/var/log/nero-*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 nero nero
}

/var/log/nero-backup.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    create 0640 nero nero
}
```

## Telegram Notification Script

```bash
#!/bin/bash
# notify-telegram.sh
# Send a message to Telegram
# Usage: ./notify-telegram.sh "Message text"
#        echo "Message" | ./notify-telegram.sh

set -euo pipefail

# Load credentials from .env
if [ -f "$HOME/workspace/.env" ]; then
    eval "$(grep -E '^TELEGRAM_(BOT_TOKEN|CHAT_ID)=' "$HOME/workspace/.env")"
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:?Set TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID:?Set TELEGRAM_CHAT_ID}"

# Get message from argument or stdin
if [ -n "${1:-}" ]; then
    MESSAGE="$1"
else
    MESSAGE=$(cat)
fi

# Truncate if too long (Telegram limit is 4096 chars)
if [ ${#MESSAGE} -gt 4000 ]; then
    MESSAGE="${MESSAGE:0:3990}...(truncated)"
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MESSAGE" \
    -d parse_mode="Markdown" \
    -d disable_web_page_preview="true" > /dev/null
```

## FLOW Hourly Monitor

```bash
#!/bin/bash
# flow-hourly.sh
# FLOW-style hourly health monitor
# Only alerts when problems are detected

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

# Check API
if ! curl -sf --max-time 10 http://127.0.0.1:8100/health > /dev/null 2>&1; then
    add_issue "API health check failed"
fi

# Check disk space
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -gt 90 ]; then
    add_issue "Disk usage: ${DISK_PCT}%"
fi

# Check memory
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
if [ "$MEM_AVAIL" -lt 500 ]; then
    add_issue "Low memory: ${MEM_AVAIL}MB available"
fi

# Check for recent OOM kills
OOM_COUNT=$(journalctl -k --since "1 hour ago" --no-pager 2>/dev/null | grep -c "Out of memory" || true)
if [ "$OOM_COUNT" -gt 0 ]; then
    add_issue "OOM killer triggered $OOM_COUNT times in last hour"
fi

# Report
if [ -n "$ISSUES" ]; then
    echo -e "FLOW ALERT $(hostname) $(date '+%H:%M'):\n$ISSUES" | \
        /usr/local/bin/notify-telegram.sh
    echo "$(date) ISSUES:$(echo -e "$ISSUES")"
else
    echo "$(date) All OK"
fi
```

## FLOW Daily Report

```bash
#!/bin/bash
# flow-send-daily.sh
# FLOW-style daily status report sent to Telegram

set -euo pipefail

REPORT=""
add() { REPORT="${REPORT}$1\n"; }

add "*Daily Report: $(date '+%Y-%m-%d %H:%M')*"
add "Host: $(hostname)"
add ""

# Uptime
add "*Uptime:* $(uptime -p)"
add ""

# Service status
add "*Services:*"
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    STATUS=$(systemctl --user is-active "$svc" 2>/dev/null || echo "unknown")
    MEM=$(systemctl --user show "$svc" -p MemoryCurrent --value 2>/dev/null || echo "0")
    MEM_MB=$((MEM / 1048576))
    add "  $svc: $STATUS (${MEM_MB}MB)"
done
add ""

# Docker
add "*Docker:*"
docker ps --format "  {{.Names}}: {{.Status}}" 2>/dev/null | while read line; do add "$line"; done
add ""

# Resources
add "*Resources:*"
add "  CPU: $(awk '{printf "%.1f", $1}' /proc/loadavg) load ($(nproc) cores)"
add "  RAM: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
add "  Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
add "  Swap: $(free -h | awk '/Swap:/ {print $3 "/" $2}')"
add ""

# Recent errors (last 24h)
ERROR_COUNT=$(journalctl --user -u 'nero-*' --since "24 hours ago" -p err --no-pager 2>/dev/null | wc -l)
add "*Errors (24h):* $ERROR_COUNT"

# Backup status
LAST_BACKUP=$(ls -td /home/nero/backups/20* 2>/dev/null | head -1)
if [ -n "$LAST_BACKUP" ]; then
    AGE_H=$(( ($(date +%s) - $(stat -c %Y "$LAST_BACKUP")) / 3600 ))
    SIZE=$(du -sh "$LAST_BACKUP" | cut -f1)
    add "*Backup:* $(basename "$LAST_BACKUP") ($SIZE, ${AGE_H}h ago)"
else
    add "*Backup:* NONE FOUND"
fi

echo -e "$REPORT" | /usr/local/bin/notify-telegram.sh
```

## Cron Schedule for Monitoring

```cron
# === FLOW Monitoring ===

# Hourly health check (alert only on problems)
0 * * * * /home/nero/workspace/scripts/flow-hourly.sh >> /var/log/nero-flow.log 2>&1

# Daily report (22:00)
0 22 * * * /home/nero/workspace/scripts/flow-send-daily.sh >> /var/log/nero-flow.log 2>&1

# Weekly report (Monday 7:00)
0 7 * * 1 /home/nero/workspace/scripts/flow-send-weekly.sh >> /var/log/nero-flow.log 2>&1

# Startup heartbeat
@reboot sleep 5 && /home/nero/workspace/scripts/startup-heartbeat.sh >> /var/log/nero-startup.log 2>&1
```
