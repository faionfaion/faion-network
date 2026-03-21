# Health Checks and Auto-Heal Examples

## Example 1: NERO Auto-Heal Watcher

The NERO platform uses a Python watcher (watcher.py) running as a systemd service that monitors all services and auto-restarts failures.

### Watcher Service Setup

```bash
# Install watcher
$ cp ~/workspace/scripts/watcher.py /srv/nero/watcher.py

# Create systemd service
$ cat > ~/.config/systemd/user/nero-watcher.service << 'EOF'
[Unit]
Description=NERO Auto-Heal Watcher
After=nero-core.service nero-channel-web.service

[Service]
Type=simple
ExecStart=/srv/nero/nero-core/.venv/bin/python3 /srv/nero/watcher.py
Restart=always
RestartSec=10
MemoryMax=256M
OOMScoreAdjust=-800

[Install]
WantedBy=default.target
EOF

$ systemctl --user daemon-reload
$ systemctl --user enable --now nero-watcher
```

### Normal Operation Logs

```
2026-03-21 10:00:00 [INFO] watcher: Auto-heal watcher started (interval=60s, cooldown=300s)
2026-03-21 10:00:00 [INFO] watcher: Monitoring 4 services: nero-core, nero-channel-web, nero-channel-tg, nero-web
2026-03-21 10:01:00 [DEBUG] watcher: nero-core: healthy
2026-03-21 10:01:00 [DEBUG] watcher: nero-channel-web: healthy
2026-03-21 10:01:00 [DEBUG] watcher: nero-channel-tg: healthy
2026-03-21 10:01:00 [DEBUG] watcher: nero-web: healthy
2026-03-21 10:02:00 [DEBUG] watcher: nero-core: healthy
...
```

### Auto-Heal in Action

```
# nero-channel-tg crashes due to Telegram API rate limit
2026-03-21 14:30:00 [WARNING] watcher: nero-channel-tg: unhealthy (failures=1)
2026-03-21 14:31:00 [WARNING] watcher: nero-channel-tg: unhealthy (failures=2)
2026-03-21 14:31:00 [WARNING] watcher: nero-channel-tg: restarting...
2026-03-21 14:31:01 [INFO] watcher: nero-channel-tg: restart command succeeded
2026-03-21 14:32:00 [DEBUG] watcher: nero-channel-tg: healthy
```

### Max Restarts Exceeded

```
# nero-core keeps crashing (bad code deployed)
2026-03-21 15:00:00 [WARNING] watcher: nero-core: unhealthy (failures=2)
2026-03-21 15:00:00 [WARNING] watcher: nero-core: restarting...
2026-03-21 15:00:01 [INFO] watcher: nero-core: restart command succeeded
2026-03-21 15:01:00 [WARNING] watcher: nero-core: unhealthy (failures=2)
2026-03-21 15:06:00 [WARNING] watcher: nero-core: restarting...    # After 5min cooldown
2026-03-21 15:06:01 [INFO] watcher: nero-core: restart command succeeded
2026-03-21 15:07:00 [WARNING] watcher: nero-core: unhealthy (failures=2)
2026-03-21 15:12:00 [WARNING] watcher: nero-core: restarting...    # 3rd restart
2026-03-21 15:13:00 [WARNING] watcher: nero-core: unhealthy (failures=2)
2026-03-21 15:13:00 [ERROR] watcher: nero-core: max restarts (3/hour) reached
2026-03-21 15:13:00 [WARNING] watcher: ALERT: nero-core is unhealthy and cannot be auto-restarted. Failures: 2, Restarts this hour: 3
# Alert sent via Telegram - manual intervention required
```

## Example 2: FastAPI /health Endpoint in nero-channel-web

```python
# nero_channel_web/routes/health.py
import asyncio
import time

from fastapi import APIRouter, Response

router = APIRouter()
START_TIME = time.time()


async def _check_db(pool):
    try:
        start = time.time()
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def _check_redis(redis):
    try:
        start = time.time()
        await redis.ping()
        return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def _check_rabbitmq(connection):
    try:
        start = time.time()
        if connection and not connection.is_closed:
            return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
        return {"status": "error", "error": "Connection closed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.get("/health")
async def health(response: Response):
    from nero_channel_web.deps import get_db_pool, get_redis, get_rabbitmq

    checks = {}
    db_result, redis_result, rmq_result = await asyncio.gather(
        _check_db(get_db_pool()),
        _check_redis(get_redis()),
        _check_rabbitmq(get_rabbitmq()),
        return_exceptions=True,
    )

    checks["database"] = db_result if not isinstance(db_result, Exception) else {"status": "error"}
    checks["redis"] = redis_result if not isinstance(redis_result, Exception) else {"status": "error"}
    checks["rabbitmq"] = rmq_result if not isinstance(rmq_result, Exception) else {"status": "error"}

    all_ok = all(c.get("status") == "ok" for c in checks.values())
    status = "ok" if all_ok else "degraded"

    if not all_ok:
        response.status_code = 503

    return {
        "status": status,
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME),
        "checks": checks,
    }


@router.get("/health/live")
async def health_live():
    return Response(status_code=200)
```

### Healthy Response

```bash
$ curl -s http://127.0.0.1:8100/health | jq
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 86423,
  "checks": {
    "database": {
      "status": "ok",
      "latency_ms": 1.2
    },
    "redis": {
      "status": "ok",
      "latency_ms": 0.3
    },
    "rabbitmq": {
      "status": "ok",
      "latency_ms": 0.8
    }
  }
}
```

### Degraded Response (Redis Down)

```bash
$ curl -s http://127.0.0.1:8100/health | jq
{
  "status": "degraded",
  "version": "1.0.0",
  "uptime_seconds": 86500,
  "checks": {
    "database": {
      "status": "ok",
      "latency_ms": 1.5
    },
    "redis": {
      "status": "error",
      "error": "Connection refused"
    },
    "rabbitmq": {
      "status": "ok",
      "latency_ms": 1.1
    }
  }
}
# HTTP Status: 503
```

## Example 3: Docker HEALTHCHECK in nero-infra

```yaml
# ~/workspace/repos/nero-infra/docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    container_name: nero-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: nero
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: nero
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nero"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    ports:
      - "127.0.0.1:5432:5432"

  redis:
    image: redis:7-alpine
    container_name: nero-redis
    restart: unless-stopped
    command: redis-server --maxmemory 1536mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    ports:
      - "127.0.0.1:6379:6379"

  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: nero-rabbitmq
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: nero
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
      RABBITMQ_DEFAULT_VHOST: nero
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    ports:
      - "127.0.0.1:5672:5672"
      - "127.0.0.1:15672:15672"
```

### Checking Docker Health Status

```bash
$ docker ps --format "table {{.Names}}\t{{.Status}}"
NAMES            STATUS
nero-postgres    Up 3 days (healthy)
nero-redis       Up 3 days (healthy)
nero-rabbitmq    Up 3 days (healthy)
nero-flower      Up 3 days

$ docker inspect nero-postgres --format '{{json .State.Health.Status}}'
"healthy"

$ docker inspect nero-postgres --format '{{json .State.Health.Log}}' | jq '.[0]'
{
  "Start": "2026-03-21T10:00:00.000000Z",
  "End": "2026-03-21T10:00:00.050000Z",
  "ExitCode": 0,
  "Output": "/var/run/postgresql:5432 - accepting connections\n"
}
```

## Example 4: Celery Worker Health Check

```bash
# Check if workers are alive and processing
$ /srv/nero/nero-core/.venv/bin/celery -A nero_core inspect ping
-> worker1@nero-hetzner: OK
        pong

# Check active tasks
$ /srv/nero/nero-core/.venv/bin/celery -A nero_core inspect active
-> worker1@nero-hetzner: OK
    * {'id': 'abc-123', 'name': 'nero_core.tasks.process_message',
       'args': '()', 'kwargs': '{...}', 'started': 1711015200.0}

# Check queue depth (are messages piling up?)
$ curl -s -u nero:$RABBITMQ_PASSWORD http://localhost:15672/api/queues/%2Fnero/celery | jq '.messages'
0

# If queue depth is growing, workers may be stuck
$ curl -s -u nero:$RABBITMQ_PASSWORD http://localhost:15672/api/queues/%2Fnero/celery | jq '.messages'
47  # Bad! Messages are piling up

# Check worker stats for clues
$ /srv/nero/nero-core/.venv/bin/celery -A nero_core inspect stats | grep -A5 "pool"
    "pool": {
        "max-concurrency": 4,
        "processes": [12345, 12346, 12347, 12348],
        "max-tasks-per-child": "N/A",
        "timeouts": [0, 0]
    }
```

## Example 5: Alerting via Telegram

```bash
# Test alert
$ bash /srv/nero/alert.sh "Test alert: NERO health check system is working"

# Check Telegram - message received:
# [nero-hetzner] 2026-03-21 10:00:00 UTC
# Test alert: NERO health check system is working

# Real alert from watcher (when nero-core crashes):
# [nero-hetzner] 2026-03-21 15:13:00 UTC
# nero-core is unhealthy and cannot be auto-restarted.
# Failures: 2, Restarts this hour: 3
```
