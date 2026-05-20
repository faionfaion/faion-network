---
slug: health-checks-autoheal
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Health monitoring and automatic recovery for multi-service platforms on Ubuntu 24.
content_id: "abd4c6d7d0c27da9"
tags: [health-checks, monitoring, systemd, auto-heal, ubuntu]
---
# Health Checks and Auto-Heal for Multi-Service Platforms

## Summary

**One-sentence:** Health monitoring and automatic recovery for multi-service platforms on Ubuntu 24.

**One-paragraph:** Health monitoring and automatic recovery for multi-service platforms on Ubuntu 24.04 VPS. Three layers: HTTP /health endpoints (liveness + readiness with dependency checks), systemd watchdog (Type=notify, WatchdogSec=30s, application sends WATCHDOG=1 every 15s), and an auto-heal watcher process (checks all services every 60s, restarts on 2+ consecutive failures, 5-min cooldown, max 3 restarts/hour, sends Telegram alerts).

## Applies If (ALL must hold)

- Multi-service platforms where a Celery worker, API, or bot can silently fail
- Services that can hang (respond to systemd but stop processing) — systemd alone won't catch these
- After deploy: confirming all services pass health probes before marking deploy successful
- Implementing /health endpoints in FastAPI/Django services for external monitoring integration

## Skip If (ANY kills it)

- Simple single-service deployments where Restart=always in systemd is sufficient
- Managed platforms (Heroku, Railway, Render) that provide built-in health check restarts
- As a replacement for proper structured logging — health checks detect failure, logs explain it
- Setting WatchdogSec below 10s — application must notify at half the interval; too short causes false positives under load

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
