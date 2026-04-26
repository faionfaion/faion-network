# Cron Automation

## Summary

Linux cron scheduling patterns for VPS platforms: script structure (lock + log + trap + env), crontab management, flock-based overlap prevention, environment handling, and FLOW-style multi-frequency monitoring (hourly silent health check → daily/weekly reports). Every production cron script must use `set -euo pipefail`, a `flock` lock file, a log function, and a `trap cleanup EXIT`.

## Why

Cron runs with a minimal environment (`PATH=/usr/bin:/bin`, no `.bashrc`) and produces no output visible to the operator unless explicitly redirected. Scripts that work manually fail silently in cron because of missing PATH, unloaded env vars, and no lock preventing overlapping runs. The FLOW pattern structures monitoring at increasing detail per cadence so hourly checks are silent on success (no alert fatigue) while daily/weekly reports always fire.

## When To Use

- Scheduling recurring server-side tasks: backups, log cleanup, health checks, report delivery
- Implementing FLOW-style multi-frequency autonomous monitoring (hourly/daily/weekly cadence)
- Running post-deploy hooks or config sync at a fixed cadence
- Draining queues or syncing files at a fixed interval
- `@reboot` tasks that must start when the server boots

## When NOT To Use

- Tasks needing reliable missed-run recovery → use systemd timers (`Persistent=true`)
- Application-level scheduling tied to Django/Celery → use Celery Beat
- Tasks needing resource limits (CPU cap, memory max) → systemd timer with `MemoryMax=`
- Dependency ordering between tasks → systemd `After=`/`Wants=`
- Sub-minute scheduling → cron minimum resolution is 1 min; use a loop service

## Content

| File | What's inside |
|------|---------------|
| `content/01-script-patterns.xml` | Standard cron script template: set -euo pipefail, flock, log, trap, source env; common gotchas |
| `content/02-schedule-reference.xml` | Cron syntax, common schedule expressions, crontab header setup, cron vs systemd timer comparison |
| `content/03-flow-monitoring.xml` | FLOW multi-frequency pattern: hourly silent / daily-weekly always-send; schedule examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/cron-script.sh` | Production-ready cron script template with all required patterns |
| `templates/crontab.txt` | Complete crontab with header, FLOW monitoring, backup, and maintenance entries |
