# Monitoring & Logging Examples

## Example 1: NERO Platform Monitoring Stack

The NERO platform uses a lightweight, script-based monitoring approach with FLOW-style autonomous reports.

### Monitoring Architecture

```
FLOW System:
  Hourly  -> health check -> alert only on problems (Telegram)
  Daily   -> full report   -> Telegram daily summary
  Weekly  -> trends report -> Telegram weekly summary
  Monthly -> capacity      -> Telegram monthly review

Always-On:
  nero-autoheal.service -> watches services, restarts on failure
  tmux status bar       -> CPU/MEM/disk at a glance

On-Demand:
  health-check.sh       -> manual full health check
  tmux-system.sh        -> monitoring dashboard
```

### FLOW Hourly Output (Normal)

```
# /var/log/nero-flow.log
2026-03-21 10:00:01 All OK
2026-03-21 11:00:01 All OK
2026-03-21 12:00:01 All OK
```

### FLOW Hourly Output (Problem Detected)

```
# /var/log/nero-flow.log
2026-03-21 13:00:01 ISSUES:- nero-core is DOWN
- API health check failed

# Telegram message sent:
# FLOW ALERT nero 13:00:
# - nero-core is DOWN
# - API health check failed
```

### FLOW Daily Report (Telegram)

```
*Daily Report: 2026-03-21 22:00*
Host: nero

*Uptime:* up 15 days, 3 hours

*Services:*
  nero-core: active (847MB)
  nero-channel-web: active (185MB)
  nero-channel-tg: active (92MB)
  nero-web: active (45MB)
  nero-beat: active (78MB)
  nero-autoheal: active (35MB)

*Docker:*
  nero-postgres: Up 15 days (healthy)
  nero-redis: Up 15 days (healthy)
  nero-rabbitmq: Up 15 days (healthy)
  nero-flower: Up 15 days

*Resources:*
  CPU: 1.2 load (16 cores)
  RAM: 8.5G/30G
  Disk: 45G/155G (29%)
  Swap: 0B/4.0G

*Errors (24h):* 3
*Backup:* 20260321_030000 (285MB, 19h ago)
```

---

## Example 2: nero-autoheal Service

A lightweight Python service that monitors critical services and restarts them on failure.

### How It Works

```
Every 60 seconds:
  1. Check each monitored service (systemctl --user is-active)
  2. Check each Docker container (docker inspect)
  3. Check API endpoint (curl health)
  4. If service down:
     a. Log the failure
     b. Attempt restart (systemctl --user restart)
     c. Wait 10 seconds
     d. Verify restart worked
     e. Send Telegram alert
  5. If restart fails after 3 attempts:
     a. Send critical alert
     b. Stop trying (avoid restart storm)
```

### systemd Service

```ini
# ~/.config/systemd/user/nero-autoheal.service
[Unit]
Description=NERO Auto-Heal Watcher
After=nero-core.service nero-channel-web.service

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-core
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/srv/nero/nero-core/.venv/bin/python -m src.autoheal
Restart=on-failure
RestartSec=30
MemoryMax=128M

[Install]
WantedBy=default.target
```

### Shell-based Alternative

```bash
#!/bin/bash
# autoheal.sh - Simple auto-heal loop
# Run as systemd service or in tmux

set -euo pipefail

MONITOR_SERVICES=(nero-core nero-channel-web nero-channel-tg nero-web nero-beat)
CHECK_INTERVAL=60
MAX_RESTARTS=3
RESTART_COUNTS=()

# Initialize restart counters
for i in "${!MONITOR_SERVICES[@]}"; do
    RESTART_COUNTS[$i]=0
done

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1"; }

while true; do
    for i in "${!MONITOR_SERVICES[@]}"; do
        svc="${MONITOR_SERVICES[$i]}"

        if systemctl --user is-active --quiet "$svc" 2>/dev/null; then
            # Service is healthy, reset counter
            RESTART_COUNTS[$i]=0
            continue
        fi

        # Service is down
        log "ALERT: $svc is DOWN"

        if [ "${RESTART_COUNTS[$i]}" -ge "$MAX_RESTARTS" ]; then
            log "CRITICAL: $svc failed $MAX_RESTARTS restarts, not retrying"
            continue
        fi

        # Attempt restart
        RESTART_COUNTS[$i]=$((RESTART_COUNTS[$i] + 1))
        log "Restarting $svc (attempt ${RESTART_COUNTS[$i]}/$MAX_RESTARTS)..."
        systemctl --user restart "$svc" 2>/dev/null || true

        sleep 5

        if systemctl --user is-active --quiet "$svc" 2>/dev/null; then
            log "OK: $svc restarted successfully"
            /usr/local/bin/notify-telegram.sh \
                "AUTOHEAL: *$svc* was down, restarted successfully" 2>/dev/null || true
        else
            log "FAIL: $svc did not restart"
            /usr/local/bin/notify-telegram.sh \
                "AUTOHEAL FAIL: *$svc* could not be restarted (attempt ${RESTART_COUNTS[$i]}/$MAX_RESTARTS)" 2>/dev/null || true
        fi
    done

    sleep "$CHECK_INTERVAL"
done
```

---

## Example 3: Log Analysis Patterns

Common journalctl queries for troubleshooting.

### Find Errors in Last Hour

```bash
# All nero service errors
journalctl --user -u 'nero-*' -p err --since "1 hour ago" --no-pager

# Count errors per service
for svc in nero-core nero-channel-web nero-channel-tg; do
    count=$(journalctl --user -u "$svc" -p err --since "1 hour ago" --no-pager 2>/dev/null | wc -l)
    echo "$svc: $count errors"
done
```

### Find OOM Kills

```bash
# Kernel OOM killer events
journalctl -k | grep -i "out of memory"

# systemd MemoryMax enforcement
journalctl --user | grep -i "memory"

# Which process was killed
dmesg | grep -i "killed process"
```

### Find Service Restarts

```bash
# Service restart events
journalctl --user -u nero-core | grep -E "(Started|Stopped|Failed)"

# Count restarts today
journalctl --user -u nero-core --since today | grep "Started" | wc -l
```

### Slow Query Detection (PostgreSQL)

```bash
# PostgreSQL slow queries (if log_min_duration_statement is set)
docker logs nero-postgres 2>&1 | grep "duration:" | tail -20

# Active queries
docker exec nero-postgres psql -U nero -d nero_db -c "
    SELECT pid, now() - pg_stat_activity.query_start AS duration, query
    FROM pg_stat_activity
    WHERE state != 'idle'
    ORDER BY duration DESC;
"
```

---

## Example 4: Startup Heartbeat

Send a Telegram notification when the server boots, confirming services are up.

```bash
#!/bin/bash
# startup-heartbeat.sh
# Run at boot: @reboot sleep 5 && /path/to/startup-heartbeat.sh

set -euo pipefail

# Load env for Telegram credentials
source /home/nero/workspace/.env 2>/dev/null || true

# Wait for services to stabilize
sleep 30

# Collect status
SERVICES_OK=0
SERVICES_FAIL=0
STATUS=""

for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    if systemctl --user is-active --quiet "$svc" 2>/dev/null; then
        STATUS="${STATUS}  $svc: UP\n"
        SERVICES_OK=$((SERVICES_OK + 1))
    else
        STATUS="${STATUS}  $svc: DOWN\n"
        SERVICES_FAIL=$((SERVICES_FAIL + 1))
    fi
done

DOCKER_OK=0
for ct in nero-postgres nero-redis nero-rabbitmq; do
    if docker inspect -f '{{.State.Running}}' "$ct" 2>/dev/null | grep -q true; then
        DOCKER_OK=$((DOCKER_OK + 1))
    fi
done

MSG="*Server Booted: $(hostname)*
$(date '+%Y-%m-%d %H:%M:%S')

*Services:* ${SERVICES_OK} up, ${SERVICES_FAIL} down
$(echo -e "$STATUS")
*Docker:* ${DOCKER_OK}/3 containers running
*Uptime:* $(uptime -p)
*Load:* $(awk '{print $1}' /proc/loadavg)"

echo -e "$MSG" | /usr/local/bin/notify-telegram.sh
echo "$(date) Startup heartbeat sent"
```

---

## Example 5: Disk Usage Monitor

Track disk usage trends and alert before problems.

```bash
#!/bin/bash
# disk-monitor.sh
# Track disk usage and identify large consumers

set -euo pipefail

echo "=== Disk Usage Report: $(date '+%Y-%m-%d %H:%M') ==="
echo ""

# Overall usage
echo "--- Filesystems ---"
df -h / /var/lib/docker 2>/dev/null | column -t
echo ""

# Docker usage
echo "--- Docker ---"
docker system df 2>/dev/null
echo ""

# Largest directories
echo "--- Top 10 Directories (/) ---"
sudo du -sh /home /var /srv /tmp /usr 2>/dev/null | sort -rh | head -10
echo ""

# Docker volumes
echo "--- Docker Volumes ---"
docker volume ls -q | while read vol; do
    SIZE=$(docker run --rm -v "$vol":/data alpine du -sh /data 2>/dev/null | cut -f1)
    echo "  $vol: $SIZE"
done
echo ""

# Journal usage
echo "--- Journal ---"
journalctl --disk-usage
echo ""

# Log files
echo "--- Log Files (>10MB) ---"
sudo find /var/log -type f -size +10M -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $NF}'
```
