# Monitoring & Logging

Lightweight monitoring and logging for solo developer VPS platforms. Covers journalctl patterns, log rotation, tmux-based status dashboards, health check scripts, alerting via Telegram, FLOW-style autonomous monitoring, and process monitoring -- all without heavy monitoring stacks (no Prometheus/Grafana needed for a single server).

## Overview

Solo developer servers do not need enterprise monitoring. A few scripts, journald configuration, and Telegram alerts provide 95% of the monitoring value at 1% of the complexity.

| Approach | Complexity | Good For |
|----------|-----------|----------|
| journalctl + scripts | Low | Single server, solo dev |
| tmux status dashboard | Low | At-a-glance monitoring |
| Telegram alerts | Low | Immediate failure notification |
| FLOW-style reports | Medium | Periodic autonomous health checks |
| Prometheus + Grafana | High | Multi-server, team, SLOs |

## journalctl Patterns

### Viewing Logs

```bash
# All logs from current boot
journalctl -b

# Specific service (system)
journalctl -u nginx

# Specific user service
journalctl --user -u nero-core

# Follow in real-time
journalctl --user -u nero-core -f

# Since a time
journalctl --user -u nero-core --since "2 hours ago"
journalctl --user -u nero-core --since "2026-03-21 10:00:00"

# Error priority and above
journalctl --user -u nero-core -p err

# Combined multiple services
journalctl --user -u nero-core -u nero-channel-web -u nero-channel-tg

# Output as JSON (for parsing)
journalctl --user -u nero-core -o json --since "1 hour ago"

# Show only messages (no metadata)
journalctl --user -u nero-core -o cat

# Kernel messages (OOM, hardware)
journalctl -k --since "1 hour ago"

# Boot messages
journalctl --list-boots
journalctl -b -1  # Previous boot
```

### Common Filters

| Filter | Purpose | Example |
|--------|---------|---------|
| `-u` | System unit | `-u nginx` |
| `--user -u` | User unit | `--user -u nero-core` |
| `-p` | Priority level | `-p err` (err, warning, info, debug) |
| `--since` | Start time | `--since "1 hour ago"` |
| `--until` | End time | `--until "2026-03-21 12:00"` |
| `-f` | Follow | Real-time tail |
| `-n` | Last N lines | `-n 50` |
| `-o` | Output format | `-o json`, `-o cat`, `-o short-iso` |
| `--no-pager` | Don't paginate | For scripts |
| `-b` | Boot | `-b -1` (previous boot) |
| `-k` | Kernel messages | dmesg equivalent |
| `--disk-usage` | Storage used | Check journal size |

## Log Rotation

### journald Configuration

```ini
# /etc/systemd/journald.conf
[Journal]
# Maximum disk usage for persistent logs
SystemMaxUse=2G

# Maximum disk usage for runtime (volatile) logs
RuntimeMaxUse=500M

# Maximum individual log file size
SystemMaxFileSize=100M

# Retention period
MaxRetentionSec=30d

# Compress logs
Compress=yes

# Storage (persistent = survives reboot)
Storage=persistent
```

After changes: `sudo systemctl restart systemd-journald`

### logrotate for Application Logs

```
# /etc/logrotate.d/nero-platform
/var/log/nero-*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 nero nero
    sharedscripts
    postrotate
        # Signal applications to reopen log files if needed
        systemctl --user -M nero@ reload nero-core 2>/dev/null || true
    endscript
}
```

### Docker Log Rotation

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## tmux Status Monitoring

A tmux status bar showing real-time system stats.

### System Stats in tmux Status Bar

```bash
# ~/.tmux.conf additions
set -g status-right-length 120
set -g status-right '#[fg=green]CPU:#{cpu_percentage} #[fg=yellow]MEM:#{ram_percentage} #[fg=cyan]#(df -h / | tail -1 | awk "{print $5}") #[fg=white]%H:%M'
```

### tmux Session with System Dashboard

```bash
#!/bin/bash
# tmux-system.sh
# Create a tmux session with system monitoring panes

SESSION="system"
tmux kill-session -t "$SESSION" 2>/dev/null

tmux new-session -d -s "$SESSION" -n "monitor"

# Top pane: htop
tmux send-keys "htop" C-m

# Bottom-left: service status (refreshes every 30s)
tmux split-window -v -l 15
tmux send-keys "watch -n 30 'systemctl --user status nero-* --no-pager 2>/dev/null | grep -E \"(nero-|Active|Memory)\"'" C-m

# Bottom-right: docker stats
tmux split-window -h
tmux send-keys "docker stats --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'" C-m

tmux select-pane -t 0
tmux attach -t "$SESSION"
```

## Health Check Scripts

### Comprehensive Health Check

```bash
#!/bin/bash
# health-check.sh
# Check all NERO platform services and infrastructure

set -euo pipefail

ERRORS=0
WARNINGS=0

check() {
    local name="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo "OK   $name"
    else
        echo "FAIL $name"
        ERRORS=$((ERRORS + 1))
    fi
}

warn() {
    local name="$1"
    local msg="$2"
    echo "WARN $name: $msg"
    WARNINGS=$((WARNINGS + 1))
}

echo "=== Health Check: $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

# --- Infrastructure (Docker) ---
echo "--- Infrastructure ---"
check "Docker daemon" "systemctl is-active docker"
check "PostgreSQL" "docker exec nero-postgres pg_isready -U nero"
check "Redis" "docker exec nero-redis redis-cli ping"
check "RabbitMQ" "docker exec nero-rabbitmq rabbitmq-diagnostics -q ping"

# --- Application Services ---
echo ""
echo "--- Applications ---"
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    check "$svc" "systemctl --user is-active $svc"
done

# --- Endpoints ---
echo ""
echo "--- Endpoints ---"
check "API health" "curl -sf http://127.0.0.1:8100/health"
check "Web frontend" "curl -sf http://127.0.0.1:8101/ -o /dev/null"

# --- Resources ---
echo ""
echo "--- Resources ---"
DISK_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_USAGE" -gt 90 ]; then
    warn "Disk" "${DISK_USAGE}% used (>90%)"
elif [ "$DISK_USAGE" -gt 80 ]; then
    warn "Disk" "${DISK_USAGE}% used (>80%)"
else
    echo "OK   Disk: ${DISK_USAGE}% used"
fi

MEM_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    warn "Memory" "${MEM_USAGE}% used (>90%)"
else
    echo "OK   Memory: ${MEM_USAGE}% used"
fi

LOAD=$(cat /proc/loadavg | awk '{print $1}')
CPUS=$(nproc)
LOAD_PCT=$(echo "$LOAD $CPUS" | awk '{printf "%.0f", ($1/$2)*100}')
if [ "$LOAD_PCT" -gt 80 ]; then
    warn "CPU Load" "$LOAD (${LOAD_PCT}% of ${CPUS} CPUs)"
else
    echo "OK   CPU Load: $LOAD (${LOAD_PCT}% of ${CPUS} CPUs)"
fi

# --- Summary ---
echo ""
echo "=== Summary: $ERRORS errors, $WARNINGS warnings ==="
exit $ERRORS
```

## Alerting via Telegram

### Send Alert Function

```bash
#!/bin/bash
# notify-telegram.sh
# Send a message to Telegram
# Usage: echo "message" | ./notify-telegram.sh
#        ./notify-telegram.sh "message text"

set -euo pipefail

# Load from .env or set directly
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"

if [ -n "${1:-}" ]; then
    MESSAGE="$1"
else
    MESSAGE=$(cat)
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MESSAGE" \
    -d parse_mode="Markdown" > /dev/null
```

### Alert-on-Failure Wrapper

```bash
#!/bin/bash
# alert-on-failure.sh
# Run a command, alert if it fails
# Usage: ./alert-on-failure.sh "Backup" /path/to/backup.sh

TASK_NAME="${1:?Usage: $0 <task-name> <command> [args...]}"
shift

if ! "$@" 2>&1; then
    /usr/local/bin/notify-telegram.sh "ALERT: *$TASK_NAME* failed on $(hostname) at $(date '+%H:%M')"
fi
```

## FLOW-Style Autonomous Monitoring

FLOW is a pattern where the server autonomously monitors itself at regular intervals and sends periodic reports.

### Schedule

| Frequency | Purpose | Cron |
|-----------|---------|------|
| Hourly | Quick health check, log anomalies | `0 * * * *` |
| Every 3 hours | Summary of hourly checks | `5 6,9,12,15,18,21 * * *` |
| Daily (22:00) | Full daily report | `0 22 * * *` |
| Weekly (Mon 7:00) | Weekly trends, capacity | `0 7 * * 1` |
| Monthly (1st 7:15) | Monthly review, costs | `15 7 1 * *` |
| Quarterly | Strategic review | `20 7 1 1,4,7,10 *` |
| Annual (Jan 1) | Yearly summary | `25 7 1 1 *` |

### Hourly Health Script

```bash
#!/bin/bash
# flow-hourly.sh
# Quick health check, only alert on problems

set -euo pipefail

ISSUES=""

# Check critical services
for svc in nero-core nero-channel-web nero-channel-tg; do
    if ! systemctl --user is-active --quiet "$svc" 2>/dev/null; then
        ISSUES="$ISSUES\n- $svc is DOWN"
    fi
done

# Check Docker containers
for container in nero-postgres nero-redis nero-rabbitmq; do
    if ! docker inspect -f '{{.State.Running}}' "$container" 2>/dev/null | grep -q true; then
        ISSUES="$ISSUES\n- $container is DOWN"
    fi
done

# Check disk space
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -gt 90 ]; then
    ISSUES="$ISSUES\n- Disk usage: ${DISK_PCT}%"
fi

# Check API
if ! curl -sf --max-time 5 http://127.0.0.1:8100/health > /dev/null 2>&1; then
    ISSUES="$ISSUES\n- API health check failed"
fi

# Alert only if issues found
if [ -n "$ISSUES" ]; then
    echo -e "FLOW ALERT $(date '+%H:%M'):\n$ISSUES" | /usr/local/bin/notify-telegram.sh
    echo "$(date) ISSUES FOUND:$ISSUES"
else
    echo "$(date) All systems OK"
fi
```

## Process Monitoring

### Check for Zombie Processes

```bash
# Count zombie processes
ps aux | awk '$8=="Z"' | wc -l

# List zombie processes
ps aux | awk '$8=="Z" {print $2, $11}'
```

### Monitor Memory by Process

```bash
# Top memory consumers
ps aux --sort=-%mem | head -15

# Memory for specific process group
ps aux | grep "[n]ero" | awk '{sum+=$6} END {printf "NERO total RSS: %.0f MB\n", sum/1024}'
```

### Open File Descriptors

```bash
# System-wide
cat /proc/sys/fs/file-nr
# output: used  unused  max

# Per process
ls /proc/$(pgrep -f nero-core | head -1)/fd | wc -l

# Top open files
lsof | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

## Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Journal too large | `journalctl --disk-usage` | Set SystemMaxUse in journald.conf |
| Docker logs filling disk | Large log files | Configure daemon.json log rotation |
| OOM kill not logged | Need kernel messages | `journalctl -k \| grep -i oom` |
| Logs missing after reboot | Volatile storage | Set `Storage=persistent` in journald.conf |
| Telegram alert not sending | Bot token or chat ID wrong | Test with curl directly |

## Related Methodologies

- `health-checks-autoheal/` -- automated service restart on failure
- `cron-automation/` -- scheduling monitoring scripts
- `systemd-user-services/` -- services being monitored
- `tmux-power-user/` -- tmux dashboard setup
