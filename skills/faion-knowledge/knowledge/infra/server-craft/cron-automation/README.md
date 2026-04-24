# Cron Automation

Cron job patterns, scheduling, error handling, and FLOW-style autonomous monitoring for VPS platforms. Covers cron syntax, crontab management, script best practices, locking with flock, environment handling, systemd timers as an alternative, and multi-frequency monitoring patterns.

## Overview

Cron is the standard task scheduler on Linux. For solo developer platforms, cron handles backups, monitoring, cleanup, and autonomous reporting without the overhead of more complex scheduling systems.

| Tool | Complexity | Use Case |
|------|-----------|----------|
| cron | Low | Simple scheduled tasks |
| systemd timers | Medium | Tasks needing dependency, logging, resources |
| Celery Beat | High | Application-level scheduling |

## Cron Syntax

```
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12)
# |  |  |  |  .---- day of week (0 - 7, 0 and 7 = Sunday)
# |  |  |  |  |
# *  *  *  *  *  command
```

### Common Patterns

| Schedule | Expression | Description |
|----------|-----------|-------------|
| Every minute | `* * * * *` | Run continuously |
| Every 5 minutes | `*/5 * * * *` | Frequent polling |
| Every 15 minutes | `*/15 * * * *` | Regular sync |
| Every hour | `0 * * * *` | Hourly at :00 |
| Every day at 3 AM | `0 3 * * *` | Nightly jobs |
| Every Monday at 7 AM | `0 7 * * 1` | Weekly report |
| First of month at 7:15 | `15 7 1 * *` | Monthly tasks |
| Weekdays at 9 AM | `0 9 * * 1-5` | Business hours |
| On boot | `@reboot` | Startup tasks |

### Special Strings

| String | Equivalent | Meaning |
|--------|-----------|---------|
| `@reboot` | N/A | Run once at boot |
| `@hourly` | `0 * * * *` | Every hour |
| `@daily` | `0 0 * * *` | Every day at midnight |
| `@weekly` | `0 0 * * 0` | Every Sunday at midnight |
| `@monthly` | `0 0 1 * *` | First of month |
| `@yearly` | `0 0 1 1 *` | January 1st |

## Crontab Management

```bash
# Edit crontab for current user
crontab -e

# List current crontab
crontab -l

# Remove all cron jobs
crontab -r

# Install crontab from file
crontab crontab.txt

# Edit crontab for another user (as root)
sudo crontab -u nero -e
```

## Cron Script Best Practices

### Essential Patterns

Every cron script should follow these patterns:

```bash
#!/bin/bash
# script-name.sh
# Description of what this script does
# Cron: 0 3 * * * /path/to/script-name.sh

set -euo pipefail

# 1. Logging
LOG_FILE="/var/log/nero-scriptname.log"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"; }

# 2. Lock file (prevent overlapping runs)
LOCK_FILE="/tmp/scriptname.lock"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "ERROR: Another instance is already running"
    exit 1
fi

# 3. Error handling with cleanup
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log "ERROR: Script failed with exit code $exit_code"
        # Optional: send alert
    fi
}
trap cleanup EXIT

# 4. Load environment
source /home/nero/workspace/.env 2>/dev/null || true

# 5. Main logic
log "Starting..."
# ... do work ...
log "Done"
```

### Pattern Breakdown

| Pattern | Why | How |
|---------|-----|-----|
| `set -euo pipefail` | Fail fast on errors | Shell option |
| Logging | Track execution history | Append to log file |
| flock | Prevent overlapping runs | File-based locking |
| trap/cleanup | Handle failures | Shell trap |
| Source .env | Load secrets/config | Source file |

## Locking with flock

`flock` prevents multiple instances of the same script from running simultaneously.

```bash
# Method 1: flock in script (recommended)
exec 9>/tmp/myscript.lock
if ! flock -n 9; then
    echo "Another instance is running"
    exit 1
fi

# Method 2: flock wrapper (from crontab)
# In crontab:
* * * * * flock -n /tmp/myscript.lock /path/to/myscript.sh

# Method 3: flock with timeout
exec 9>/tmp/myscript.lock
if ! flock -w 30 9; then
    echo "Could not acquire lock within 30 seconds"
    exit 1
fi
```

| Flag | Meaning |
|------|---------|
| `-n` | Non-blocking (fail immediately if locked) |
| `-w N` | Wait up to N seconds for lock |
| `-s` | Shared lock (multiple readers) |
| `-x` | Exclusive lock (default) |

## Environment in Cron

Cron runs with a minimal environment. Common issues:

| Variable | In Shell | In Cron | Fix |
|----------|----------|---------|-----|
| PATH | Full user PATH | `/usr/bin:/bin` | Set PATH in crontab |
| HOME | User home | User home | Usually fine |
| SHELL | /bin/bash | /bin/sh | Set SHELL in crontab |
| DISPLAY | Set | Not set | Not needed for server |
| USER | Set | Set | Usually fine |

### Fix: Set Variables at Top of Crontab

```cron
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=""

# Jobs below this line use bash and full PATH
0 3 * * * /home/nero/workspace/scripts/backup.sh
```

### Fix: Source Environment in Script

```bash
#!/bin/bash
# Load user environment
source /home/nero/.bashrc 2>/dev/null || true
source /home/nero/workspace/.env 2>/dev/null || true

# Now PATH, secrets, etc. are available
```

## systemd Timers vs Cron

| Feature | cron | systemd timers |
|---------|------|---------------|
| Configuration | Single crontab file | Pair of .timer + .service files |
| Logging | Manual (redirect to file) | Automatic (journald) |
| Dependencies | None | After=, Wants= |
| Resource limits | None | MemoryMax=, CPUQuota= |
| Missed runs | Lost | Persistent=true (catches up) |
| Random delay | None | RandomizedDelaySec= |
| Monitoring | `crontab -l` | `systemctl list-timers` |

### When to Use Each

| Use cron when... | Use systemd timer when... |
|------------------|--------------------------|
| Simple scripts | Need journald logging |
| Quick to set up | Need resource limits |
| Familiar syntax | Need dependency ordering |
| Portable | Need missed-run recovery |

## FLOW-Style Monitoring

FLOW is a multi-frequency autonomous monitoring pattern where the server monitors itself at increasing levels of detail.

### Schedule Hierarchy

```
Hourly    -> Quick health check (alert only on problems)
Every 3h  -> Summarize recent checks
Daily     -> Full status report
Weekly    -> Trends and capacity planning
Monthly   -> Infrastructure review
Quarterly -> Strategic review
Annual    -> Yearly summary
```

### Implementation

```cron
# FLOW Monitoring Schedule
0 * * * * /home/nero/workspace/scripts/flow-hourly.sh >> /var/log/nero-flow.log 2>&1
5 6,9,12,15,18,21 * * * /home/nero/workspace/scripts/flow-summarize.sh >> /var/log/nero-flow.log 2>&1
0 22 * * * /home/nero/workspace/scripts/flow-send-daily.sh >> /var/log/nero-flow.log 2>&1
0 7 * * 1 /home/nero/workspace/scripts/flow-send-weekly.sh >> /var/log/nero-flow.log 2>&1
15 7 1 * * /home/nero/workspace/scripts/flow-send-monthly.sh >> /var/log/nero-flow.log 2>&1
20 7 1 1,4,7,10 * /home/nero/workspace/scripts/flow-send-quarterly.sh >> /var/log/nero-flow.log 2>&1
25 7 1 1 * /home/nero/workspace/scripts/flow-send-annual.sh >> /var/log/nero-flow.log 2>&1
```

### Key Principle: Hourly is Silent on Success

The hourly check should only send alerts when problems are detected. Daily/weekly reports always send regardless.

## Common Cron Jobs for VPS Platforms

| Job | Schedule | Purpose |
|-----|----------|---------|
| Database backup | `0 3 * * *` | Nightly PostgreSQL dump |
| Log rotation check | `0 4 * * *` | Verify logs are rotated |
| Docker cleanup | `0 5 * * 0` | Weekly container/image prune |
| Certificate check | `0 9 * * *` | Check SSL expiry |
| Health check | `0 * * * *` | Hourly service monitoring |
| Config sync | `*/15 * * * *` | Sync config files |
| Startup heartbeat | `@reboot` | Notify on server boot |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Job not running | Wrong PATH in cron | Set PATH in crontab header |
| Script works manually but not in cron | Environment differences | Source .bashrc/.env in script |
| Job runs twice | Duplicate crontab entries | `crontab -l` and deduplicate |
| Output not captured | Missing redirect | Append `>> /var/log/name.log 2>&1` |
| Job overlaps itself | Long-running job | Use flock |
| Wrong timezone | Cron uses system TZ | Check `timedatectl` |
| @reboot not firing | cron daemon not running | `systemctl status cron` |

## Related Methodologies

- `monitoring-logging/` -- what monitoring scripts do
- `backup-recovery/` -- backup cron jobs
- `systemd-user-services/` -- timer units as alternative to cron
