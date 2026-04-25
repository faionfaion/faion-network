# Agent Integration — Health Checks and Auto-Heal

## When to use
- Platform has multiple services and manual monitoring is not feasible for a solo developer
- A service crashes silently (no alert, users report issues hours later)
- Adding `/health` and `/health/ready` endpoints to a new FastAPI or Django service
- Setting up systemd watchdog for a long-running process
- Implementing Celery worker health verification in an auto-heal watcher
- Configuring Docker HEALTHCHECK for compose services used as dependencies

## When NOT to use
- Single-service deployments where systemd `Restart=always` is sufficient
- Managed platforms (Heroku, Railway) that have built-in health checks and auto-restart
- Ephemeral jobs or batch processes — health checks are designed for long-running daemons
- When the service already has a dedicated monitoring solution (Datadog, New Relic) — adding a custom watcher creates redundancy without value

## Where it fails / limitations
- The auto-heal watcher itself is a single point of failure — if the watcher crashes, no other service is monitored; the watcher must have `Restart=always` and be monitored by systemd
- Deep health checks that call external dependencies (DB, Redis) can themselves become slow or fail when those dependencies are overloaded — separate liveness (`/health/live`) from readiness (`/health/ready`) to avoid cascading failures
- `MAX_RESTARTS` per hour prevents restart loops, but also means a repeatedly crashing service stops being healed — the operator must receive an alert when max restarts are reached
- systemd watchdog requires `Type=notify` in the service unit — uvicorn/gunicorn do not send watchdog pings automatically; a background asyncio task must do it
- Celery `inspect ping` has a 10-second default timeout — if the broker (RabbitMQ, Redis) is slow, the health check blocks; set an explicit timeout
- Circuit breakers implemented in-process are reset on service restart — state is not shared across workers or instances

## Agentic workflow
An agent implements health monitoring by: (1) adding a `/health` endpoint to the application code using the FastAPI template from this methodology, (2) writing the auto-heal watcher script with the appropriate `ServiceCheck` entries for all platform services, (3) creating the systemd unit for the watcher, and (4) enabling the watcher service. The agent should verify end-to-end by hitting the health endpoint with `curl` and checking that `systemctl --user status nero-watcher` shows active. After any service restart test, the agent checks watcher logs for the restart action.

### Recommended subagents
- `faion-sdd-executor-agent` — execute monitoring setup as part of a platform health SDD feature

### Prompt pattern
```
Add a /health endpoint to the FastAPI app at src/main.py.
Checks required:
- PostgreSQL: SELECT 1 via asyncpg pool
- Redis: PING via redis-asyncio
- RabbitMQ: GET /api/healthchecks/node via aiohttp (port 15672, auth from env)
Response: JSON with status (ok/degraded), uptime_seconds, per-check latency_ms.
Return 503 if any check fails.
```

```
Write an auto-heal watcher for these services:
- nero-core: Celery workers (celery inspect ping, app=nero_core, venv=/srv/nero/nero-core/.venv)
- nero-channel-web: HTTP health check at http://127.0.0.1:8100/health
- nero-channel-tg: systemd unit nero-channel-tg.service
Watcher settings: check interval 60s, max 3 restarts per service per hour, cooldown 300s.
Output: watcher.py and the systemd service unit file.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `systemctl --user` | Manage user-scope systemd services | Built-in |
| `journalctl --user -u` | Stream service logs | Built-in |
| `celery inspect ping` | Check Celery worker liveness | `pip install celery` |
| `curl` | HTTP health endpoint testing | Built-in |
| `sd_notify` / `systemd-notify` | Send watchdog pings from shell scripts | `apt install systemd` (built-in) |
| `rabbitmq-diagnostics` | RabbitMQ health check from inside container | Built-in in official image |
| `redis-cli ping` | Redis health check | `apt install redis-tools` |
| `pg_isready` | PostgreSQL health check | `apt install postgresql-client` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RabbitMQ Management API | OSS | Yes | REST API at port 15672; `/api/healthchecks/node` returns `{"status":"ok"}` |
| Prometheus + Alertmanager | OSS | Partial | Full monitoring stack; overkill for solo VPS; use only if multiple servers |
| UptimeRobot | SaaS (free tier) | Yes | External HTTP monitor with Telegram/email alerts; free plan checks every 5 minutes |
| Better Uptime | SaaS | Yes | HTTP + heartbeat monitoring; REST API for managing monitors |
| Healthchecks.io | SaaS (OSS self-host) | Yes | Cron/heartbeat monitoring; agent sends a ping, service alerts if ping stops |
| Flower | OSS | Yes | Celery monitoring web UI; exposes REST API for worker and task status |

## Templates & scripts
See templates.md for complete watcher implementation. Key systemd watchdog integration for uvicorn:

```python
# Add to FastAPI app startup — watchdog_task.py
import asyncio
import os
import socket

def notify_systemd_watchdog():
    """Send WATCHDOG=1 to systemd notify socket."""
    sock_path = os.environ.get("NOTIFY_SOCKET")
    if not sock_path:
        return
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
            # Abstract socket: path starts with @
            addr = "\0" + sock_path[1:] if sock_path.startswith("@") else sock_path
            sock.connect(addr)
            sock.send(b"WATCHDOG=1")
    except OSError:
        pass

async def watchdog_loop(interval: float = 15.0):
    """Background task — ping watchdog at half the WatchdogSec interval."""
    while True:
        notify_systemd_watchdog()
        await asyncio.sleep(interval)

# In your lifespan or startup event:
# asyncio.create_task(watchdog_loop(interval=15.0))
```

## Best practices
- Separate `/health/live` (fast, no deps) from `/health/ready` (full dependency check) — load balancers use live, dependent services use ready
- Implement restart cooldown in the watcher (`RESTART_COOLDOWN = 300`) to prevent flapping when a dependency (RabbitMQ) is temporarily unavailable
- Always alert (Telegram, email) when `MAX_RESTARTS` is reached — at that point the watcher has given up and human intervention is required
- Set Docker HEALTHCHECK `start_period` generously (30-60s) for services with slow initialization; prematurely failed health checks cause `depends_on: condition: service_healthy` to never resolve
- Run the watcher as a systemd user service with `Restart=always` and `RestartSec=10` — if the watcher crashes, it restarts within 10 seconds
- Use `asyncio.gather` for parallel dependency checks in `/health/ready` — sequential checks multiply latency under load
- Log every restart action with timestamp and reason — this creates an audit trail for post-mortem analysis

## AI-agent gotchas
- Agent must not use `subprocess.run("systemctl restart ...", shell=True)` inside the watcher without a cooldown guard — a cascading failure will trigger rapid restart loops, potentially crashing the host
- Celery `inspect ping` blocks for up to 10 seconds if workers are unreachable; the watcher must use `timeout=10` and catch `TimeoutError` as an unhealthy signal
- The health endpoint must not require authentication — external monitoring services and internal watchers hit it without credentials; use a separate authenticated endpoint for detailed diagnostic data
- `systemctl --user restart` only works when `$XDG_RUNTIME_DIR` is set and the user session is active; inside a system-level service, use `systemctl --user --runtime-dir=...` or switch to system-level services
- Docker health check status is separate from container running status — `docker ps` shows "Up" even if HEALTHCHECK is "unhealthy"; agent must parse `docker inspect --format '{{.State.Health.Status}}'`
- The `/health` endpoint itself can become a DDoS vector if it triggers expensive DB queries on every request — cache the result for 5-10 seconds or use a separate lightweight liveness check

## References
- https://www.freedesktop.org/software/systemd/man/sd_notify.html
- https://docs.celeryq.dev/en/stable/userguide/monitoring.html#inspection
- https://www.rabbitmq.com/monitoring.html
- https://docs.docker.com/engine/reference/builder/#healthcheck
- https://healthchecks.io/
- https://uptimerobot.com/
