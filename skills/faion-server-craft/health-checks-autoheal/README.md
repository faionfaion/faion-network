# Health Checks and Auto-Heal

## Overview

Health monitoring and automatic recovery for multi-service platforms running on VPS. Covers HTTP health endpoints, systemd watchdog integration, custom auto-heal watcher scripts, circuit breaker patterns, Docker HEALTHCHECK, Celery worker inspection, RabbitMQ management API health checks, and alerting. Designed for platforms where manual intervention should be minimized.

**Target:** Ubuntu 24.04 VPS running multiple systemd user services (FastAPI, Celery, Telegram bot) with Docker backing services.

## When to Use

| Scenario | Fit |
|----------|-----|
| Services crash and nobody notices | Essential |
| Celery workers stop processing tasks | Essential |
| Need automatic service recovery | Essential |
| Implementing /health endpoints in APIs | Recommended |
| Monitoring backing services (DB, Redis, RabbitMQ) | Recommended |
| Setting up watchdog timers for services | Recommended |
| Building custom monitoring dashboards | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Health endpoint** | HTTP endpoint (/health) returning service status |
| **Liveness check** | Is the process alive and responding? |
| **Readiness check** | Is the service ready to handle requests? |
| **Watchdog** | systemd mechanism that kills service if it stops reporting |
| **Auto-heal** | Automatic restart of failed services without human intervention |
| **Circuit breaker** | Pattern that stops calling a failing dependency |
| **Deep health check** | Verifies all dependencies (DB, Redis, MQ) are accessible |

## HTTP Health Endpoints

### Endpoint Design

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `/health` | Quick liveness check | `{"status": "ok"}` |
| `/health/ready` | Full readiness check | `{"status": "ok", "checks": {...}}` |
| `/health/live` | Simple alive check | `200 OK` (no body) |

### Response Format

```json
{
    "status": "ok",
    "version": "1.2.3",
    "uptime_seconds": 3600,
    "checks": {
        "database": {"status": "ok", "latency_ms": 2.1},
        "redis": {"status": "ok", "latency_ms": 0.5},
        "rabbitmq": {"status": "ok", "latency_ms": 1.2}
    }
}
```

### Degraded Response

```json
{
    "status": "degraded",
    "version": "1.2.3",
    "checks": {
        "database": {"status": "ok", "latency_ms": 2.1},
        "redis": {"status": "error", "error": "Connection refused"},
        "rabbitmq": {"status": "ok", "latency_ms": 1.2}
    }
}
```

HTTP status codes:
- `200` - healthy
- `503` - unhealthy or degraded (service should not receive traffic)

### FastAPI Health Endpoint Implementation

```python
import time
import asyncio
from fastapi import FastAPI, Response

app = FastAPI()
START_TIME = time.time()

async def check_database():
    try:
        async with db_pool.acquire() as conn:
            start = time.time()
            await conn.execute("SELECT 1")
            return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}

async def check_redis():
    try:
        start = time.time()
        await redis_client.ping()
        return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/health")
async def health(response: Response):
    checks = {}
    checks["database"], checks["redis"] = await asyncio.gather(
        check_database(), check_redis()
    )

    all_ok = all(c["status"] == "ok" for c in checks.values())
    status = "ok" if all_ok else "degraded"

    if not all_ok:
        response.status_code = 503

    return {
        "status": status,
        "uptime_seconds": round(time.time() - START_TIME),
        "checks": checks,
    }

@app.get("/health/live")
async def health_live():
    return Response(status_code=200)
```

## systemd Watchdog

### How It Works

The service periodically notifies systemd it is alive. If the notification stops, systemd considers the service hung and restarts it.

### Service Configuration

```ini
# nero-channel-web.service
[Service]
Type=notify
WatchdogSec=30                    # Must notify within 30s
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5

ExecStart=/srv/nero/nero-channel-web/.venv/bin/uvicorn \
    nero_channel_web.main:app --host 127.0.0.1 --port 8100
```

### Python Watchdog Notification

```python
import os
import socket

def notify_watchdog():
    """Notify systemd watchdog that service is alive."""
    sock_path = os.environ.get("NOTIFY_SOCKET")
    if not sock_path:
        return

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        sock.connect(sock_path)
        sock.send(b"WATCHDOG=1")
    finally:
        sock.close()

# Call periodically (at half the WatchdogSec interval)
# e.g., in a background task every 15s for WatchdogSec=30
```

### Watchdog with uvicorn

For uvicorn/gunicorn, the watchdog needs a background task:

```python
import asyncio

async def watchdog_loop():
    """Background task to ping systemd watchdog."""
    while True:
        notify_watchdog()
        await asyncio.sleep(15)  # Half of WatchdogSec=30

@app.on_event("startup")
async def start_watchdog():
    asyncio.create_task(watchdog_loop())
```

## Auto-Heal Watcher

### Pattern Overview

A lightweight watcher process monitors all services and restarts any that fail health checks.

```
watcher.py (runs as systemd service)
  ├── Check nero-core (celery inspect ping)
  ├── Check nero-channel-web (HTTP /health)
  ├── Check nero-channel-tg (systemctl is-active)
  └── If check fails → systemctl --user restart <service>
```

### Watcher Implementation

```python
#!/usr/bin/env python3
"""Auto-heal watcher for NERO platform services."""

import subprocess
import time
import logging
import urllib.request
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("watcher")

CHECK_INTERVAL = 60  # seconds
MAX_RESTARTS = 3     # max restarts per service per hour
RESTART_COOLDOWN = 300  # seconds between restarts

class ServiceCheck:
    def __init__(self, name, check_fn, restart_cmd):
        self.name = name
        self.check_fn = check_fn
        self.restart_cmd = restart_cmd
        self.restart_count = 0
        self.last_restart = 0

    def is_healthy(self):
        try:
            return self.check_fn()
        except Exception as e:
            log.warning(f"{self.name} health check failed: {e}")
            return False

    def restart(self):
        now = time.time()
        if now - self.last_restart < RESTART_COOLDOWN:
            log.warning(f"{self.name}: cooldown active, skipping restart")
            return
        if self.restart_count >= MAX_RESTARTS:
            log.error(f"{self.name}: max restarts reached, manual intervention needed")
            return

        log.info(f"Restarting {self.name}...")
        subprocess.run(self.restart_cmd, shell=True, check=True)
        self.restart_count += 1
        self.last_restart = now

def check_http(url, timeout=5):
    """Check HTTP health endpoint."""
    def _check():
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read())
        return data.get("status") in ("ok", "degraded")
    return _check

def check_systemd(service_name):
    """Check systemd service is active."""
    def _check():
        result = subprocess.run(
            ["systemctl", "--user", "is-active", service_name],
            capture_output=True, text=True,
        )
        return result.stdout.strip() == "active"
    return _check

def check_celery(venv_path, app_name):
    """Check Celery workers respond to ping."""
    def _check():
        result = subprocess.run(
            [f"{venv_path}/bin/celery", "-A", app_name, "inspect", "ping"],
            capture_output=True, text=True, timeout=10,
        )
        return "pong" in result.stdout.lower()
    return _check

# Define services to monitor
SERVICES = [
    ServiceCheck(
        "nero-core",
        check_celery("/srv/nero/nero-core/.venv", "nero_core"),
        "systemctl --user restart nero-core",
    ),
    ServiceCheck(
        "nero-channel-web",
        check_http("http://127.0.0.1:8100/health"),
        "systemctl --user restart nero-channel-web",
    ),
    ServiceCheck(
        "nero-channel-tg",
        check_systemd("nero-channel-tg"),
        "systemctl --user restart nero-channel-tg",
    ),
]

def main():
    log.info("Auto-heal watcher started")
    while True:
        for svc in SERVICES:
            if not svc.is_healthy():
                log.warning(f"{svc.name} is unhealthy")
                svc.restart()
            else:
                svc.restart_count = max(0, svc.restart_count - 1)  # Decay
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
```

### Watcher systemd Service

```ini
# ~/.config/systemd/user/nero-watcher.service
[Unit]
Description=NERO Auto-Heal Watcher
After=nero-core.service nero-channel-web.service

[Service]
Type=simple
ExecStart=/srv/nero/nero-core/.venv/bin/python3 /srv/nero/watcher.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

## Docker HEALTHCHECK

### Docker Compose Health Checks

```yaml
services:
  postgres:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nero"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  rabbitmq:
    image: rabbitmq:3-management-alpine
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

## Celery Health Checks

### Celery Inspect Ping

```bash
# Check if workers are alive
celery -A nero_core inspect ping

# Check active tasks
celery -A nero_core inspect active

# Check reserved tasks (queued)
celery -A nero_core inspect reserved

# Check stats
celery -A nero_core inspect stats
```

### RabbitMQ Management API

```bash
# Check node health
curl -u guest:guest http://localhost:15672/api/healthchecks/node

# Check queue depth (alerts on buildup)
curl -u guest:guest http://localhost:15672/api/queues/%2F/celery | jq '.messages'

# Check connections
curl -u guest:guest http://localhost:15672/api/connections | jq length
```

## Circuit Breaker Pattern

### Simple Circuit Breaker

```python
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure = 0
        self.state = "closed"  # closed=normal, open=blocking, half-open=testing

    def call(self, fn, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = fn(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

## Alerting

### Simple Alert Script

```bash
#!/bin/bash
# alert.sh - Send alerts via multiple channels
# Usage: bash alert.sh "Service nero-core is down"

MESSAGE="$1"
HOSTNAME=$(hostname)
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Telegram notification
TELEGRAM_BOT_TOKEN="${TELEGRAM_ALERT_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_ALERT_CHAT_ID:-}"

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    curl -s -X POST \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=[${HOSTNAME}] ${TIMESTAMP}%0A${MESSAGE}" \
        -d "parse_mode=HTML" >/dev/null
fi

# Log locally
echo "$TIMESTAMP [$HOSTNAME] $MESSAGE" >> /var/log/nero-alerts.log
```

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [deploy-scripts](../deploy-scripts/) | Health check after deploy |
| [swap-memory-management](../swap-memory-management/) | Memory-aware health checks |
| [multi-project-hosting](../multi-project-hosting/) | Per-project health monitoring |
| [secrets-management](../secrets-management/) | Credentials for health API calls |
