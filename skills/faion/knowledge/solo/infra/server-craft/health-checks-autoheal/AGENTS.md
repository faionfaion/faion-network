# Health Checks and Auto-Heal

## Summary

Health monitoring and automatic recovery for multi-service platforms on Ubuntu 24.04 VPS. Three layers: HTTP `/health` endpoints (liveness + readiness with dependency checks), systemd watchdog (Type=notify, WatchdogSec=30s, application sends WATCHDOG=1 every 15s), and an auto-heal watcher process (checks all services every 60s, restarts on 2+ consecutive failures, 5-min cooldown, max 3 restarts/hour, sends Telegram alerts).

## Why

Solo-operated platforms have no on-call rotation. Without automatic recovery, a crashed Celery worker or hung API process stays down until the developer notices — potentially hours later. Systemd handles transient crashes (Restart=always); the watcher handles hung processes that pass systemd's is-active check but fail actual health probes.

## When To Use

- Multi-service platforms where a Celery worker, API, or bot can silently fail
- Services that can hang (respond to systemd but stop processing) — systemd alone won't catch these
- After deploy: confirming all services pass health probes before marking deploy successful
- Implementing `/health` endpoints in FastAPI/Django services for external monitoring integration

## When NOT To Use

- Simple single-service deployments where `Restart=always` in systemd is sufficient
- Managed platforms (Heroku, Railway, Render) that provide built-in health check restarts
- As a replacement for proper structured logging — health checks detect failure, logs explain it
- Setting WatchdogSec below 10s — application must notify at half the interval; too short causes false positives under load

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Liveness vs readiness, watchdog timer mechanics, auto-heal pattern, circuit breaker states |
| `content/02-implementations.xml` | FastAPI /health endpoint, Python watchdog notify, watcher ServiceCheck class, Docker HEALTHCHECK |
| `content/03-examples.xml` | NERO platform watcher config, Celery inspect ping check, RabbitMQ management API check, Telegram alerting |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-endpoint.py` | FastAPI /health with parallel DB + Redis checks, 200/503 status codes |
| `templates/watchdog-notify.py` | Python NOTIFY_SOCKET sender, background asyncio loop at WatchdogSec/2 |
| `templates/watcher.py` | Auto-heal watcher: ServiceCheck, cooldown, max restarts, Telegram alert |
| `templates/watcher.service` | systemd user service for the watcher process |
| `templates/docker-compose-healthchecks.yml` | PostgreSQL, Redis, RabbitMQ HEALTHCHECK blocks |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/health-report.sh` | Poll all service /health endpoints and systemd status, print summary table |
| `scripts/watcher-status.sh` | Show watcher log tail, restart counts, last alert timestamps |
