# systemd User Services Templates

## Python Application Service (uvicorn/FastAPI)

```ini
# ~/.config/systemd/user/myapp-web.service
[Unit]
Description=MyApp Web Server (FastAPI/uvicorn)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-web
EnvironmentFile=/home/%u/workspace/.env
ExecStart=/srv/myapp/myapp-web/.venv/bin/uvicorn \
    src.main:app \
    --host 127.0.0.1 \
    --port 8100 \
    --workers 2 \
    --loop uvloop \
    --http httptools \
    --log-level info
Restart=on-failure
RestartSec=5
StartLimitBurst=5
StartLimitIntervalSec=60

# Resource limits
MemoryMax=512M
MemoryHigh=384M
LimitNOFILE=65536

# Security hardening
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
```

## Node.js Application Service

```ini
# ~/.config/systemd/user/myapp-frontend.service
[Unit]
Description=MyApp Frontend (Node.js/serve)
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-web
ExecStart=/usr/bin/npx serve dist -l 8101 -s
Restart=on-failure
RestartSec=5

# Resource limits
MemoryMax=256M
LimitNOFILE=4096

[Install]
WantedBy=default.target
```

## Celery Worker Service

```ini
# ~/.config/systemd/user/myapp-worker.service
[Unit]
Description=MyApp Celery Worker
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-core
EnvironmentFile=/home/%u/workspace/.env
ExecStart=/srv/myapp/myapp-core/.venv/bin/celery \
    -A src.celery_app worker \
    --pool=gevent \
    --concurrency=20 \
    --loglevel=info \
    --without-heartbeat \
    --without-mingle \
    --without-gossip \
    -Q default,priority
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitIntervalSec=120

# Resource limits (Celery workers can be memory-hungry)
MemoryMax=2G
MemoryHigh=1536M
CPUQuota=400%
TasksMax=512
LimitNOFILE=65536

[Install]
WantedBy=default.target
```

## Celery Beat Scheduler Service

```ini
# ~/.config/systemd/user/myapp-beat.service
[Unit]
Description=MyApp Celery Beat Scheduler
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-core
EnvironmentFile=/home/%u/workspace/.env
ExecStart=/srv/myapp/myapp-core/.venv/bin/celery \
    -A src.celery_app beat \
    --loglevel=info \
    --schedule=/tmp/myapp-celerybeat-schedule
Restart=on-failure
RestartSec=10

# Beat is lightweight
MemoryMax=256M

[Install]
WantedBy=default.target
```

## Telegram Bot Service (aiogram)

```ini
# ~/.config/systemd/user/myapp-tg.service
[Unit]
Description=MyApp Telegram Bot (aiogram)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-channel-tg
EnvironmentFile=/home/%u/workspace/.env
ExecStart=/srv/myapp/myapp-channel-tg/.venv/bin/python -m src.main
Restart=on-failure
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=300

# Telegram bot is lightweight
MemoryMax=256M
LimitNOFILE=4096

[Install]
WantedBy=default.target
```

## Auto-Heal Watcher Service

```ini
# ~/.config/systemd/user/myapp-autoheal.service
[Unit]
Description=MyApp Auto-Heal Watcher
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-core
EnvironmentFile=/home/%u/workspace/.env
ExecStart=/srv/myapp/myapp-core/.venv/bin/python -m src.autoheal
Restart=on-failure
RestartSec=30

# Very lightweight monitoring process
MemoryMax=128M

[Install]
WantedBy=default.target
```

## Timer Unit Template

```ini
# ~/.config/systemd/user/backup-db.timer
[Unit]
Description=Daily database backup timer

[Timer]
# Run at 3 AM every day
OnCalendar=*-*-* 03:00:00

# Catch up on missed runs (e.g., server was off)
Persistent=true

# Add random delay to avoid thundering herd
RandomizedDelaySec=300

# Accuracy (how precise the timer needs to be)
AccuracySec=1min

[Install]
WantedBy=timers.target
```

```ini
# ~/.config/systemd/user/backup-db.service
# Paired with backup-db.timer (same name prefix)
[Unit]
Description=Daily database backup

[Service]
Type=oneshot
ExecStart=/home/%u/workspace/scripts/backup-db.sh
EnvironmentFile=/home/%u/workspace/.env

# Timeout for backup operation
TimeoutStartSec=600

# No restart for oneshot
Restart=no
```

## Service with Pre/Post Commands

```ini
# ~/.config/systemd/user/myapp-web.service
[Unit]
Description=MyApp Web with Pre/Post hooks
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/myapp/myapp-web
EnvironmentFile=/home/%u/workspace/.env

# Run before starting (migrations, health checks)
ExecStartPre=/srv/myapp/myapp-web/.venv/bin/python -c "import src; print('Module OK')"

# Main process
ExecStart=/srv/myapp/myapp-web/.venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8100

# Run after start
ExecStartPost=/usr/bin/curl -sf http://127.0.0.1:8100/health || true

# Graceful stop
ExecStop=/bin/kill -SIGTERM $MAINPID
TimeoutStopSec=30

Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

## Service Override (Drop-in)

To override specific directives without editing the original file:

```bash
# Create override directory
mkdir -p ~/.config/systemd/user/myapp-worker.service.d/

# Create override file
cat > ~/.config/systemd/user/myapp-worker.service.d/memory.conf << 'EOF'
[Service]
# Override memory limit for this environment
MemoryMax=4G
MemoryHigh=3G
EOF

systemctl --user daemon-reload
```

## Target Unit (Service Group)

```ini
# ~/.config/systemd/user/myapp.target
# Group all myapp services under a single target
[Unit]
Description=MyApp Platform Services
Wants=myapp-web.service myapp-worker.service myapp-beat.service myapp-tg.service

[Install]
WantedBy=default.target
```

Usage:
```bash
# Start all services in the target
systemctl --user start myapp.target

# Stop all
systemctl --user stop myapp.target

# Check status
systemctl --user status myapp.target
```

## Install Script

```bash
#!/bin/bash
# install-services.sh
# Install or update systemd user service files

set -euo pipefail

SERVICE_DIR="$HOME/.config/systemd/user"
SOURCE_DIR="${1:?Usage: $0 <source-dir-with-service-files>}"

mkdir -p "$SERVICE_DIR"

echo "=== Installing systemd user services ==="

for file in "$SOURCE_DIR"/*.service "$SOURCE_DIR"/*.timer; do
    [ -f "$file" ] || continue
    name=$(basename "$file")
    echo "  Installing: $name"
    cp "$file" "$SERVICE_DIR/$name"
done

echo ""
echo "Reloading systemd daemon..."
systemctl --user daemon-reload

echo ""
echo "Installed services:"
ls -la "$SERVICE_DIR"/*.service "$SERVICE_DIR"/*.timer 2>/dev/null

echo ""
echo "Remember to enable services:"
echo "  systemctl --user enable --now service-name.service"
```
