---
slug: cron-automation
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Linux cron scheduling patterns for VPS platforms: script structure (lock + log + trap + env), crontab management, flock-based overlap prevention, environment handling, and FLOW-style multi-frequency monitoring (hourly silent health check → daily/weekly reports).
content_id: "f565a5cfd6973968"
tags: [cron, scheduling, automation, bash, production]
---
# Cron Automation

## Summary

**One-sentence:** Linux cron scheduling patterns for VPS platforms: script structure (lock + log + trap + env), crontab management, flock-based overlap prevention, environment handling, and FLOW-style multi-frequency monitoring (hourly silent health check → daily/weekly reports).

**One-paragraph:** Linux cron scheduling patterns for VPS platforms: script structure (lock + log + trap + env), crontab management, flock-based overlap prevention, environment handling, and FLOW-style multi-frequency monitoring (hourly silent health check → daily/weekly reports). Every production cron script must use `set -euo pipefail`, a `flock` lock file, a log function, and a `trap cleanup EXIT`.

## Applies If (ALL must hold)

- Scheduling recurring server-side tasks: backups, log cleanup, health checks, report delivery
- Implementing FLOW-style multi-frequency autonomous monitoring (hourly/daily/weekly cadence)
- Running post-deploy hooks or config sync at a fixed cadence
- Draining queues or syncing files at a fixed interval
- `@reboot` tasks that must start when the server boots

## Skip If (ANY kills it)

- Tasks needing reliable missed-run recovery → use systemd timers (`Persistent=true`)
- Application-level scheduling tied to Django/Celery → use Celery Beat
- Tasks needing resource limits (CPU cap, memory max) → systemd timer with `MemoryMax=`
- Dependency ordering between tasks → systemd `After=`/`Wants=`
- Sub-minute scheduling → cron minimum resolution is 1 min; use a loop service

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
