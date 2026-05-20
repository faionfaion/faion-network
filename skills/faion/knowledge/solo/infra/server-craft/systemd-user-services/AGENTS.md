---
slug: systemd-user-services
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run applications as systemd user services (without root) with proper restart policies, resource limits, environment variables, and boot persistence.
content_id: "4203c589bba7bf3c"
tags: [systemd, services, user-services, deployment, logging]
---
# systemd User Services

## Summary

**One-sentence:** Run applications as systemd user services (without root) with proper restart policies, resource limits, environment variables, and boot persistence.

**One-paragraph:** Run applications as systemd user services (without root) with proper restart policies, resource limits, environment variables, and boot persistence. Enable linger, use absolute paths in ExecStart, set MemoryMax/MemoryHigh/CPUQuota, and replace cron with timer units for scheduled tasks.

## Applies If (ALL must hold)

- Deploying Python/Node/Go applications that must restart on crash and start at boot
- Managing multiple per-user services (Celery, FastAPI, Telegram bot) independently
- Applying MemoryMax/CPUQuota resource limits to a service that has been OOM-killed
- Adding scheduled tasks with better logging than cron (timer units)
- Replacing screen/nohup patterns with proper lifecycle management

## Skip If (ANY kills it)

- Services that must bind ports below 1024 — use nginx reverse proxy instead
- Containerized workloads managed by Docker Compose — compose restart policies replace unit files
- One-shot scripts run on demand — use cron or explicit invocation
- When sudo -u or su is used to run the service — systemctl --user requires an active user session or explicit XDG_RUNTIME_DIR

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/infra/server-craft/`
