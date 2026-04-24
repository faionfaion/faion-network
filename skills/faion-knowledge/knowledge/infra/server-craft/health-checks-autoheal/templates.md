# Health Checks and Auto-Heal Templates

## health-check.sh

Standalone health check script for all services.

```bash
#!/bin/bash
# health-check.sh - Check health of all NERO platform services
# Usage: bash health-check.sh [--verbose]
# Exit: 0=all healthy, 1=one or more unhealthy
set -euo pipefail

VERBOSE="${1:-}"
HEALTHY=0
UNHEALTHY=0

check() {
    local name="$1"
    local cmd="$2"
    if eval "$cmd" >/dev/null 2>&1; then
        [ "$VERBOSE" = "--verbose" ] && echo "[OK]   $name"
        ((HEALTHY++))
    else
        echo "[FAIL] $name"
        ((UNHEALTHY++))
    fi
}

echo "=== Health Check: $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# systemd services
check "nero-core (systemd)" \
    "systemctl --user is-active nero-core"

check "nero-channel-web (systemd)" \
    "systemctl --user is-active nero-channel-web"

check "nero-channel-tg (systemd)" \
    "systemctl --user is-active nero-channel-tg"

check "nero-web (systemd)" \
    "systemctl --user is-active nero-web"

# HTTP health endpoints
check "nero-channel-web (HTTP /health)" \
    "curl -sf http://127.0.0.1:8100/health"

# Docker services
check "PostgreSQL (Docker)" \
    "docker exec nero-postgres pg_isready -U nero"

check "Redis (Docker)" \
    "docker exec nero-redis redis-cli ping"

check "RabbitMQ (Docker)" \
    "docker exec nero-rabbitmq rabbitmq-diagnostics check_running"

# Celery workers
check "Celery workers (ping)" \
    "/srv/nero/nero-core/.venv/bin/celery -A nero_core inspect ping --timeout 10"

echo ""
echo "Results: $HEALTHY healthy, $UNHEALTHY unhealthy"

if [ "$UNHEALTHY" -gt 0 ]; then
    exit 1
fi
```

## autoheal-watcher.py

Production-quality auto-heal watcher service.

```python
#!/usr/bin/env python3
"""Auto-heal watcher for NERO platform services.

Periodically checks service health and automatically restarts
services that fail health checks. Includes cooldown periods
and maximum restart limits to prevent restart loops.

Usage:
    python3 watcher.py
    # Or as systemd service: see nero-watcher.service
"""

import json
import logging
import subprocess
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Optional

# ============================================================
# Configuration
# ============================================================
CHECK_INTERVAL = 60        # Seconds between check cycles
RESTART_COOLDOWN = 300     # Seconds between restarts of same service
MAX_RESTARTS_PER_HOUR = 3  # Max restarts per service per hour
ALERT_SCRIPT = None        # Path to alert script, or None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("watcher")


# ============================================================
# Health Check Functions
# ============================================================
def check_http(url: str, timeout: int = 5) -> bool:
    """Check HTTP health endpoint returns 2xx."""
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=timeout)
        if resp.status == 200:
            data = json.loads(resp.read())
            return data.get("status") in ("ok", "degraded")
        return False
    except Exception:
        return False


def check_systemd(unit: str) -> bool:
    """Check systemd user service is active."""
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", unit],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip() == "active"
    except Exception:
        return False


def check_celery(venv: str, app: str) -> bool:
    """Check Celery workers respond to ping."""
    try:
        result = subprocess.run(
            [f"{venv}/bin/celery", "-A", app, "inspect", "ping", "--timeout", "10"],
            capture_output=True, text=True, timeout=15,
        )
        return "pong" in result.stdout.lower()
    except Exception:
        return False


def check_docker(container: str, cmd: list[str]) -> bool:
    """Check Docker container health."""
    try:
        result = subprocess.run(
            ["docker", "exec", container] + cmd,
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


# ============================================================
# Service Definition
# ============================================================
@dataclass
class Service:
    name: str
    check_fn: Callable[[], bool]
    restart_cmd: str
    restart_count: int = 0
    last_restart: float = 0.0
    consecutive_failures: int = 0
    restart_history: list = field(default_factory=list)

    def is_healthy(self) -> bool:
        try:
            healthy = self.check_fn()
            if healthy:
                self.consecutive_failures = 0
            else:
                self.consecutive_failures += 1
            return healthy
        except Exception as e:
            log.warning(f"{self.name}: check error: {e}")
            self.consecutive_failures += 1
            return False

    def can_restart(self) -> bool:
        now = time.time()

        # Cooldown check
        if now - self.last_restart < RESTART_COOLDOWN:
            log.info(f"{self.name}: cooldown active ({int(RESTART_COOLDOWN - (now - self.last_restart))}s remaining)")
            return False

        # Hourly restart limit
        one_hour_ago = now - 3600
        recent = [t for t in self.restart_history if t > one_hour_ago]
        self.restart_history = recent  # Cleanup

        if len(recent) >= MAX_RESTARTS_PER_HOUR:
            log.error(f"{self.name}: max restarts ({MAX_RESTARTS_PER_HOUR}/hour) reached")
            return False

        return True

    def restart(self) -> bool:
        if not self.can_restart():
            return False

        log.warning(f"{self.name}: restarting...")
        try:
            result = subprocess.run(
                self.restart_cmd, shell=True,
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                log.info(f"{self.name}: restart command succeeded")
            else:
                log.error(f"{self.name}: restart failed: {result.stderr}")
        except Exception as e:
            log.error(f"{self.name}: restart error: {e}")
            return False

        now = time.time()
        self.restart_count += 1
        self.last_restart = now
        self.restart_history.append(now)
        return True


# ============================================================
# Alert Function
# ============================================================
def send_alert(message: str):
    """Send alert via configured alert script."""
    if ALERT_SCRIPT:
        try:
            subprocess.run(
                ["bash", ALERT_SCRIPT, message],
                timeout=10, capture_output=True,
            )
        except Exception as e:
            log.error(f"Alert failed: {e}")
    log.warning(f"ALERT: {message}")


# ============================================================
# Service Registry
# ============================================================
SERVICES = [
    Service(
        name="nero-core",
        check_fn=lambda: check_celery("/srv/nero/nero-core/.venv", "nero_core"),
        restart_cmd="systemctl --user restart nero-core",
    ),
    Service(
        name="nero-channel-web",
        check_fn=lambda: check_http("http://127.0.0.1:8100/health"),
        restart_cmd="systemctl --user restart nero-channel-web",
    ),
    Service(
        name="nero-channel-tg",
        check_fn=lambda: check_systemd("nero-channel-tg"),
        restart_cmd="systemctl --user restart nero-channel-tg",
    ),
    Service(
        name="nero-web",
        check_fn=lambda: check_systemd("nero-web"),
        restart_cmd="systemctl --user restart nero-web",
    ),
]


# ============================================================
# Main Loop
# ============================================================
def main():
    log.info(f"Auto-heal watcher started (interval={CHECK_INTERVAL}s, cooldown={RESTART_COOLDOWN}s)")
    log.info(f"Monitoring {len(SERVICES)} services: {', '.join(s.name for s in SERVICES)}")

    while True:
        for svc in SERVICES:
            if svc.is_healthy():
                log.debug(f"{svc.name}: healthy")
            else:
                log.warning(f"{svc.name}: unhealthy (failures={svc.consecutive_failures})")

                # Only restart after 2 consecutive failures (avoid false positives)
                if svc.consecutive_failures >= 2:
                    if svc.can_restart():
                        svc.restart()
                    else:
                        send_alert(
                            f"{svc.name} is unhealthy and cannot be auto-restarted. "
                            f"Failures: {svc.consecutive_failures}, "
                            f"Restarts this hour: {len(svc.restart_history)}"
                        )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
```

## nero-watcher.service (systemd)

```ini
# ~/.config/systemd/user/nero-watcher.service
[Unit]
Description=NERO Auto-Heal Watcher
After=nero-core.service nero-channel-web.service nero-channel-tg.service

[Service]
Type=simple
ExecStart=/srv/nero/nero-core/.venv/bin/python3 /srv/nero/watcher.py
Restart=always
RestartSec=10

# Watcher itself should be lightweight
MemoryMax=256M
OOMScoreAdjust=-800

# Ensure watcher survives OOM
OOMPolicy=continue

[Install]
WantedBy=default.target
```

## systemd WatchdogSec Service Template

```ini
# Service with watchdog integration
[Unit]
Description=My Service with Watchdog

[Service]
Type=notify
WatchdogSec=30

# Process must call sd_notify(WATCHDOG=1) every 15s (half of WatchdogSec)
# If it stops notifying, systemd kills and restarts it
ExecStart=/path/to/service

# Restart policy
Restart=on-watchdog
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5

[Install]
WantedBy=default.target
```

## FastAPI Health Endpoint Template

```python
"""Health check endpoint for FastAPI services.

Add to your FastAPI application:
    from health import register_health_routes
    register_health_routes(app, db_pool=pool, redis=redis_client)
"""

import asyncio
import time
from typing import Any, Optional

from fastapi import FastAPI, Response


def register_health_routes(
    app: FastAPI,
    db_pool: Optional[Any] = None,
    redis_client: Optional[Any] = None,
    rabbitmq_url: Optional[str] = None,
):
    """Register /health and /health/live endpoints."""

    start_time = time.time()

    async def _check_db() -> dict:
        if db_pool is None:
            return {"status": "skipped"}
        try:
            start = time.time()
            async with db_pool.acquire() as conn:
                await conn.execute("SELECT 1")
            return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _check_redis() -> dict:
        if redis_client is None:
            return {"status": "skipped"}
        try:
            start = time.time()
            await redis_client.ping()
            return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @app.get("/health")
    async def health(response: Response):
        checks = {}
        results = await asyncio.gather(
            _check_db(),
            _check_redis(),
            return_exceptions=True,
        )

        checks["database"] = results[0] if not isinstance(results[0], Exception) else {"status": "error", "error": str(results[0])}
        checks["redis"] = results[1] if not isinstance(results[1], Exception) else {"status": "error", "error": str(results[1])}

        # Filter out skipped checks
        active_checks = {k: v for k, v in checks.items() if v.get("status") != "skipped"}

        all_ok = all(c["status"] == "ok" for c in active_checks.values())
        status = "ok" if all_ok else "degraded"

        if not all_ok:
            response.status_code = 503

        return {
            "status": status,
            "uptime_seconds": round(time.time() - start_time),
            "checks": checks,
        }

    @app.get("/health/live")
    async def health_live():
        return Response(status_code=200)
```

## Alert Script Template

```bash
#!/bin/bash
# alert.sh - Send alerts via Telegram and log locally
# Usage: bash alert.sh "Alert message here"
set -euo pipefail

MESSAGE="${1:?Provide alert message}"
HOSTNAME=$(hostname)
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

FULL_MESSAGE="[$HOSTNAME] $TIMESTAMP
$MESSAGE"

# ============================================================
# Telegram Alert
# ============================================================
TELEGRAM_BOT_TOKEN="${TELEGRAM_ALERT_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_ALERT_CHAT_ID:-}"

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    curl -s -X POST \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${FULL_MESSAGE}" \
        -d "parse_mode=HTML" >/dev/null 2>&1 || true
fi

# ============================================================
# Local Log
# ============================================================
LOG_FILE="/var/log/nero-alerts.log"
if [ -w "$(dirname "$LOG_FILE")" ] || [ -w "$LOG_FILE" ]; then
    echo "$FULL_MESSAGE" >> "$LOG_FILE"
else
    echo "$FULL_MESSAGE" >> "$HOME/nero-alerts.log"
fi
```

## Cron Health Check (Alternative to Watcher)

```bash
# Add to crontab: crontab -e
# Run health check every 5 minutes, alert on failure
*/5 * * * * bash /srv/nero/health-check.sh 2>&1 | grep -q "FAIL" && bash /srv/nero/alert.sh "Health check failure detected. Run: bash /srv/nero/health-check.sh --verbose"
```
