# systemd User Services

## Summary

Run applications as systemd user services (`~/.config/systemd/user/`) without root access. Enable linger (`loginctl enable-linger`) so services start at boot and survive logout. `ExecStart=` must use absolute paths; `EnvironmentFile=` loads secrets without exposing them via `systemctl show`; `MemoryMax=` and `CPUQuota=` set resource limits via cgroups v2. Put `StartLimitBurst` in `[Unit]`, not `[Service]` — the `[Service]` location is silently ignored on systemd >= 229.

## Why

Running applications with `nohup ./app &` provides no restart on crash, no resource limits, no log aggregation, and no boot persistence. User services give all of these without root, scoped to a single user account. `journalctl --user -u name` gives structured logs with timestamps. `systemctl --user edit name` creates drop-in overrides that survive unit file updates.

## When To Use

- Deploying Python/Node/Go applications that must restart on crash and start at boot
- Managing multiple per-user services (Celery, FastAPI, Telegram bot) independently
- Applying `MemoryMax`/`CPUQuota` resource limits to a service that has been OOM-killed
- Adding scheduled tasks with better logging than cron (timer units)
- Replacing `screen`/`nohup` patterns with proper lifecycle management

## When NOT To Use

- Services that must bind ports below 1024 — use nginx reverse proxy instead
- Containerized workloads managed by Docker Compose — compose restart policies replace unit files
- One-shot scripts run on demand — use cron or explicit invocation
- When `sudo -u` or `su` is used to run the service — `systemctl --user` requires an active user session or explicit `XDG_RUNTIME_DIR`

## Content

| File | What's inside |
|------|---------------|
| `content/01-unit-structure.xml` | Unit/Service/Install sections, service types, restart policies, dependency types, resource limit directives |
| `content/02-patterns.xml` | Linger, EnvironmentFile security, drop-in overrides, timer units, troubleshooting table |

## Templates

| File | Purpose |
|------|---------|
| `templates/fastapi.service` | FastAPI/uvicorn service with resource limits and security hardening |
| `templates/celery-worker.service` | Celery gevent worker with MemoryMax and CPUQuota |
| `templates/telegram-bot.service` | Lightweight aiogram bot service |
| `templates/timer-pair.service` | Timer + oneshot service for scheduled tasks |
| `templates/target.service` | Target unit grouping multiple services |
