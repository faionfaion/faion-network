# systemd User Services Examples

## Example 1: NERO Platform Services

The NERO AI platform runs 6 user services under the `nero` user account.

### Service Overview

| Service | Process | Port | Memory | Purpose |
|---------|---------|------|--------|---------|
| nero-core | Celery worker (gevent x20) | -- | 2G max | LLM message processing |
| nero-channel-web | uvicorn (FastAPI) | 8100 | 512M max | HTTP/WebSocket API |
| nero-channel-tg | aiogram bot | -- | 256M max | Telegram bridge |
| nero-web | serve (React SPA) | 8101 | 256M max | Frontend static files |
| nero-beat | Celery beat scheduler | -- | 256M max | Periodic task scheduling |
| nero-autoheal | Python watcher | -- | 128M max | Health monitoring + restart |

### nero-core.service (Celery Worker)

```ini
[Unit]
Description=NERO Core Celery Worker
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-core
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/srv/nero/nero-core/.venv/bin/celery \
    -A src.celery_app worker \
    --pool=gevent \
    --concurrency=20 \
    --loglevel=info \
    --without-heartbeat \
    --without-mingle \
    --without-gossip \
    -Q default,process_message,deliver_web,deliver_telegram
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitIntervalSec=120

MemoryMax=2G
MemoryHigh=1536M
CPUQuota=800%
TasksMax=512
LimitNOFILE=65536

[Install]
WantedBy=default.target
```

### nero-channel-web.service (FastAPI API)

```ini
[Unit]
Description=NERO Web Channel (FastAPI)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-channel-web
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/srv/nero/nero-channel-web/.venv/bin/uvicorn \
    src.main:app \
    --host 127.0.0.1 \
    --port 8100 \
    --workers 2 \
    --loop uvloop \
    --http httptools \
    --log-level info
Restart=on-failure
RestartSec=5

MemoryMax=512M
LimitNOFILE=65536

[Install]
WantedBy=default.target
```

### nero-channel-tg.service (Telegram Bot)

```ini
[Unit]
Description=NERO Telegram Channel (aiogram)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-channel-tg
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/srv/nero/nero-channel-tg/.venv/bin/python -m src.main
Restart=on-failure
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=300

MemoryMax=256M

[Install]
WantedBy=default.target
```

### nero-web.service (React SPA)

```ini
[Unit]
Description=NERO Web Frontend (React SPA)
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-web
ExecStart=/usr/bin/npx serve dist -l 8101 -s
Restart=on-failure
RestartSec=5

MemoryMax=256M

[Install]
WantedBy=default.target
```

### nero-beat.service (Celery Scheduler)

```ini
[Unit]
Description=NERO Celery Beat Scheduler
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-core
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/srv/nero/nero-core/.venv/bin/celery \
    -A src.celery_app beat \
    --loglevel=info \
    --schedule=/tmp/nero-celerybeat-schedule
Restart=on-failure
RestartSec=10

MemoryMax=256M

[Install]
WantedBy=default.target
```

### nero-autoheal.service (Health Watcher)

```ini
[Unit]
Description=NERO Auto-Heal Watcher
After=nero-core.service nero-channel-web.service
Wants=nero-core.service nero-channel-web.service

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

### Management Commands

```bash
# Enable linger (run services at boot without login)
loginctl enable-linger nero

# Enable all services
systemctl --user enable nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal

# Start all
systemctl --user start nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal

# Check all statuses
systemctl --user status 'nero-*'

# Restart just the worker after code change
systemctl --user restart nero-core

# View combined logs
journalctl --user -u nero-core -u nero-channel-web -u nero-channel-tg -f

# Check memory usage
systemctl --user status nero-core | grep Memory
# Memory: 847.3M (max: 2.0G)
```

---

## Example 2: Service with Pre-Flight Checks

A service that validates its configuration before starting.

```ini
[Unit]
Description=MyApp with Pre-Flight Checks
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp

# Pre-flight: check database connectivity
ExecStartPre=/srv/myapp/.venv/bin/python -c "from src.db import check_connection; check_connection()"

# Pre-flight: run pending migrations
ExecStartPre=/srv/myapp/.venv/bin/alembic upgrade head

# Main process
ExecStart=/srv/myapp/.venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000

# Post-start: verify health endpoint
ExecStartPost=/bin/sh -c 'sleep 2 && curl -sf http://127.0.0.1:8000/health'

EnvironmentFile=/home/nero/workspace/.env
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

---

## Example 3: Timer-Based Database Backup

Run a database backup every night at 3 AM using a systemd timer instead of cron.

### Timer Unit

```ini
# ~/.config/systemd/user/nero-backup-db.timer
[Unit]
Description=NERO Daily Database Backup

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### Service Unit

```ini
# ~/.config/systemd/user/nero-backup-db.service
[Unit]
Description=NERO Database Backup Job

[Service]
Type=oneshot
EnvironmentFile=/home/nero/workspace/.env
ExecStart=/home/nero/workspace/scripts/backup-db.sh
TimeoutStartSec=600

# Send notification on failure
ExecStopPost=/bin/sh -c 'if [ "$$EXIT_STATUS" != "0" ]; then echo "Backup failed with exit code $$EXIT_STATUS" | /usr/local/bin/notify-telegram; fi'
```

### Activation

```bash
# Enable and start timer
systemctl --user enable --now nero-backup-db.timer

# Verify timer is scheduled
systemctl --user list-timers
# NEXT                         LEFT          UNIT
# Thu 2026-03-18 03:00:00 UTC  4h left       nero-backup-db.timer

# Test backup manually
systemctl --user start nero-backup-db.service

# Check backup results
journalctl --user -u nero-backup-db.service --since today
```

---

## Example 4: Resource-Limited Development Service

A development service with strict resource limits to prevent a runaway process from consuming the entire server.

```ini
# ~/.config/systemd/user/dev-jupyter.service
[Unit]
Description=Jupyter Notebook (Development)
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/nero/notebooks
ExecStart=/home/nero/.local/bin/jupyter lab \
    --ip=127.0.0.1 \
    --port=8888 \
    --no-browser \
    --NotebookApp.token='dev-token-here'
Restart=on-failure
RestartSec=5

# Strict limits for dev workload
MemoryMax=4G
MemoryHigh=3G
CPUQuota=400%
TasksMax=128

# Kill if it exceeds memory
OOMPolicy=kill

[Install]
WantedBy=default.target
```

---

## Example 5: Watching Service Logs in tmux

A tmux layout for monitoring all NERO services at once.

```bash
#!/bin/bash
# nero-logs.sh - Open tmux with all NERO service logs

SESSION="nero-logs"

tmux kill-session -t "$SESSION" 2>/dev/null

tmux new-session -d -s "$SESSION" -n "logs"

# Top-left: nero-core
tmux send-keys "journalctl --user -u nero-core -f --no-hostname" C-m

# Top-right: nero-channel-web
tmux split-window -h
tmux send-keys "journalctl --user -u nero-channel-web -f --no-hostname" C-m

# Bottom-left: nero-channel-tg
tmux select-pane -t 0
tmux split-window -v
tmux send-keys "journalctl --user -u nero-channel-tg -f --no-hostname" C-m

# Bottom-right: all errors
tmux select-pane -t 2
tmux split-window -v
tmux send-keys "journalctl --user -u 'nero-*' -f --no-hostname -p err" C-m

tmux attach -t "$SESSION"
```

---

## Example 6: Deploying and Restarting Services

Script pattern used by the NERO deploy flow.

```bash
#!/bin/bash
# deploy-service.sh <service-name>
# Deploy code and restart a systemd user service

set -euo pipefail

SERVICE="${1:?Usage: $0 <service-name>}"
WORKSPACE="$HOME/workspace/repos/$SERVICE"
RUNTIME="/srv/nero/$SERVICE"

echo "=== Deploying $SERVICE ==="

# 1. Sync code from workspace to runtime
rsync -a --delete \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    "$WORKSPACE/src/" "$RUNTIME/src/"

# 2. Sync dependencies
rsync -a "$WORKSPACE/requirements.txt" "$RUNTIME/requirements.txt"
rsync -a "$WORKSPACE/pyproject.toml" "$RUNTIME/pyproject.toml" 2>/dev/null || true

# 3. Install dependencies if requirements changed
if ! diff -q "$WORKSPACE/requirements.txt" "$RUNTIME/.last-requirements.txt" &>/dev/null; then
    echo "  Requirements changed, installing..."
    "$RUNTIME/.venv/bin/pip" install -q -r "$RUNTIME/requirements.txt"
    cp "$RUNTIME/requirements.txt" "$RUNTIME/.last-requirements.txt"
fi

# 4. Restart service
echo "  Restarting $SERVICE..."
systemctl --user restart "$SERVICE"

# 5. Wait and verify
sleep 2
if systemctl --user is-active --quiet "$SERVICE"; then
    echo "  $SERVICE is running"
else
    echo "  ERROR: $SERVICE failed to start"
    journalctl --user -u "$SERVICE" --since "30 sec ago" --no-pager
    exit 1
fi
```
