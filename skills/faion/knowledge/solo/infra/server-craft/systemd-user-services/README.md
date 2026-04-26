# systemd User Services

Creating and managing user-level systemd services for application deployment. Covers unit file structure, dependencies, resource limits, restart policies, environment files, journald logging, linger, socket activation, and timer units.

## Overview

systemd user services run under a specific user account (not root), which is ideal for application deployments where root privileges are unnecessary and undesirable.

| Aspect | System Services | User Services |
|--------|----------------|---------------|
| Location | `/etc/systemd/system/` | `~/.config/systemd/user/` |
| Control | `sudo systemctl` | `systemctl --user` |
| Runs as | root (or specified user) | Current user |
| Starts at | Boot | User login (or with linger) |
| Logs | `journalctl -u name` | `journalctl --user -u name` |
| Ports < 1024 | Yes | No (use reverse proxy) |

## Why User Services

For solo developer platforms like NERO:

1. **No root needed** -- application code should not run as root
2. **Simple deployment** -- no sudo required to manage services
3. **Isolation** -- services scoped to user, not system-wide
4. **Linger** -- services start at boot without login, stop at shutdown
5. **Resource limits** -- per-service memory and CPU controls

## Unit File Structure

A systemd unit file has three main sections:

```ini
[Unit]
Description=Human-readable description
After=network-online.target          # Start after network is ready
Wants=network-online.target          # Soft dependency (won't fail if target is unavailable)
Requires=other.service               # Hard dependency (fails if other.service fails)

[Service]
Type=simple                          # Process type
WorkingDirectory=/path/to/app        # cd before starting
EnvironmentFile=/path/to/.env        # Load environment variables
ExecStart=/path/to/command           # Main command to run
Restart=on-failure                   # When to restart
RestartSec=5                         # Delay between restarts

[Install]
WantedBy=default.target              # Enable target (like multi-user.target for system)
```

### Unit Section

| Directive | Purpose | Values |
|-----------|---------|--------|
| Description | Human name | Free text |
| After | Start order | Space-separated targets/services |
| Wants | Soft dependency | Service names |
| Requires | Hard dependency | Service names |
| BindsTo | Like Requires, also stops when dep stops | Service names |
| PartOf | Stops/restarts with another unit | Service names |
| Conflicts | Cannot run alongside | Service names |

### Dependency Types

| Type | Meaning | On Dependency Failure |
|------|---------|----------------------|
| After | Start ordering only | No effect (just ordering) |
| Wants | Soft dependency + After | Service starts anyway |
| Requires | Hard dependency + After | Service fails to start |
| BindsTo | Like Requires | Service also stops |
| PartOf | Group management | Service stops/restarts together |

### Service Section

| Directive | Purpose | Common Values |
|-----------|---------|---------------|
| Type | Process lifecycle | simple, forking, oneshot, notify |
| ExecStart | Main command | Absolute path required |
| ExecStartPre | Run before start | Setup commands |
| ExecStartPost | Run after start | Post-start checks |
| ExecStop | Stop command | Default: SIGTERM |
| ExecReload | Reload command | e.g., `kill -HUP $MAINPID` |
| WorkingDirectory | Working dir | Absolute path |
| EnvironmentFile | Env vars file | Path to .env file |
| Environment | Inline env vars | `KEY=value` pairs |

### Service Types

| Type | Behavior | Use Case |
|------|----------|----------|
| simple | ExecStart is the main process | Most apps (uvicorn, node, celery) |
| forking | Process forks, parent exits | Traditional daemons |
| oneshot | Runs once and exits | Scripts, migrations |
| notify | Process signals readiness via sd_notify | Apps with systemd integration |
| idle | Like simple, waits for other jobs | Low-priority tasks |

### Restart Policies

| Policy | Restarts On | Use Case |
|--------|------------|----------|
| no | Never | One-shot tasks |
| on-failure | Non-zero exit, signal, timeout | Most services |
| on-abnormal | Signal, timeout, watchdog | Ignore clean exits |
| on-abort | Signal only | Crash debugging |
| always | Any exit | Critical services |

Related directives:

| Directive | Purpose | Example |
|-----------|---------|---------|
| RestartSec | Delay between restarts | 5 (seconds) |
| StartLimitBurst | Max restarts in interval | 5 |
| StartLimitIntervalSec | Interval for burst limit | 60 (seconds) |

## Resource Limits

Control memory and CPU per-service:

```ini
[Service]
# Memory limits
MemoryMax=512M                # Hard limit (OOM killed if exceeded)
MemoryHigh=384M               # Soft limit (throttled)

# CPU limits
CPUQuota=200%                 # Max CPU (200% = 2 cores)
CPUWeight=100                 # Relative weight (default 100)

# Process limits
LimitNOFILE=65536             # Max open files
TasksMax=256                  # Max child processes/threads
```

| Directive | Purpose | Notes |
|-----------|---------|-------|
| MemoryMax | Hard memory limit | Process killed if exceeded |
| MemoryHigh | Soft memory limit | Throttled, not killed |
| CPUQuota | Max CPU percentage | 100% = 1 core, 200% = 2 cores |
| CPUWeight | Relative CPU priority | 1-10000, default 100 |
| LimitNOFILE | Open file descriptor limit | Important for apps with many connections |
| TasksMax | Max threads/processes | Important for worker pools |

## Environment Files

Load environment variables from a file:

```ini
[Service]
EnvironmentFile=/home/nero/workspace/.env
```

The env file format:

```bash
# /home/nero/workspace/.env
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=info
# Comments are supported
# Empty lines are ignored
```

**Security note:** Do not use `Environment=` for secrets in unit files (visible in `systemctl show`). Use `EnvironmentFile=` instead.

## Linger

By default, user services only run while the user is logged in. Linger keeps them running after logout and starts them at boot.

```bash
# Enable linger for current user
loginctl enable-linger

# Check linger status
loginctl show-user $USER | grep Linger
# Linger=yes

# Disable linger
loginctl disable-linger
```

## journald Logging

User services log to journald automatically (stdout/stderr).

```bash
# View logs for a user service
journalctl --user -u nero-core.service

# Follow logs in real-time
journalctl --user -u nero-core.service -f

# Logs since last boot
journalctl --user -u nero-core.service -b

# Logs from last hour
journalctl --user -u nero-core.service --since "1 hour ago"

# Show only errors
journalctl --user -u nero-core.service -p err

# Multi-service logs combined
journalctl --user -u nero-core -u nero-channel-web -u nero-channel-tg
```

Configure journald log retention:

```ini
# /etc/systemd/journald.conf
[Journal]
SystemMaxUse=2G
RuntimeMaxUse=500M
MaxRetentionSec=30d
```

## Socket Activation

systemd can listen on a socket and start the service on first connection:

```ini
# nero-channel-web.socket
[Socket]
ListenStream=8100

[Install]
WantedBy=sockets.target
```

```ini
# nero-channel-web.service
[Service]
# ... normal service config
# Socket is passed as file descriptor 3
```

Useful for services that should only start when traffic arrives.

## Timer Units

systemd timers are a modern replacement for cron:

```ini
# backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=daily
Persistent=true                # Run missed events after boot
RandomizedDelaySec=300         # Random delay up to 5 minutes

[Install]
WantedBy=timers.target
```

```ini
# backup.service (paired with backup.timer)
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

### Timer Expressions

| Expression | Meaning |
|------------|---------|
| `daily` | Every day at midnight |
| `weekly` | Every Monday at midnight |
| `hourly` | Every hour |
| `*:0/15` | Every 15 minutes |
| `Mon..Fri 09:00` | Weekdays at 9 AM |
| `*-*-01 07:00` | First of every month at 7 AM |

```bash
# List active timers
systemctl --user list-timers

# Check next trigger time
systemctl --user status backup.timer
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `systemctl --user daemon-reload` | Reload unit files after changes |
| `systemctl --user start name` | Start a service |
| `systemctl --user stop name` | Stop a service |
| `systemctl --user restart name` | Restart a service |
| `systemctl --user enable name` | Enable on boot |
| `systemctl --user disable name` | Disable on boot |
| `systemctl --user status name` | Check service status |
| `systemctl --user list-units --type=service` | List running services |
| `systemctl --user show name` | Show all properties |
| `systemctl --user cat name` | Show unit file contents |
| `systemctl --user edit name` | Edit with override (drop-in) |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Service stops on logout | Linger not enabled | `loginctl enable-linger` |
| "Failed to connect to bus" | DBUS_SESSION_BUS_ADDRESS not set | Export XDG_RUNTIME_DIR and DBUS vars |
| Permission denied on port < 1024 | User services can't bind low ports | Use nginx reverse proxy |
| Service not starting at boot | Not enabled or linger off | `systemctl --user enable` + linger |
| ExecStart path not absolute | Relative paths not allowed | Use full paths |
| Env vars not loaded | Wrong EnvironmentFile path | Verify path exists, check syntax |
| OOM killed | MemoryMax too low | Increase limit or optimize app |
| Restart loop | StartLimitBurst exceeded | Fix root cause, reset with `systemctl --user reset-failed` |

## Related Methodologies

- `deploy-scripts/` -- deploying code that services run
- `monitoring-logging/` -- monitoring service health
- `health-checks-autoheal/` -- auto-restart unhealthy services
