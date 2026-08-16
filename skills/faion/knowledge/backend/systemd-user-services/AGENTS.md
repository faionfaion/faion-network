# systemd User Services

## Summary

**One-sentence:** Generates a systemd --user unit + drop-in plan (Restart, MemoryMax, EnvironmentFile, journal) for a long-running solo service — gated by `loginctl enable-linger`.

**One-paragraph:** Running services as a non-root operator via `systemd --user` is the simplest way to avoid `nohup`, `screen`, or root-owned units. This methodology pins the unit template (Restart=on-failure, RestartSec=5s, MemoryMax, EnvironmentFile, StandardOutput=journal), the linger requirement, timer pairs for periodic jobs, and a per-unit drop-in convention. Output: a UnitPlan + .service file.

**Ефективно для:**

- Long-running Python/Node apps owned by a non-root operator.
- Periodic jobs that outgrow cron (need restart-on-failure, journal logs).
- Multi-service VPS where unit drop-ins are easier than root systemctl edits.
- Replacing tmux-based 'just keep this open' patterns.

## Applies If (ALL must hold)

- Service runs ≥10 minutes per session OR continuously.
- Operator is a non-root user with linger enabled.
- Output should be journaled (not log-file-rotation-by-hand).
- Restart-on-failure semantics needed.

## Skip If (ANY kills it)

- Service runs <1 minute and is invoked ad-hoc.
- Container runtime managing process lifecycle.
- Requires capabilities only root systemd can grant (e.g. binding port 80).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service binary path + working dir | absolute paths | operator inventory |
| EnvironmentFile path (per secrets-management) | absolute path | secrets plan |
| Memory budget | MemoryHigh + MemoryMax | memory plan |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| secrets-management | EnvironmentFile path comes from secrets plan. |
| swap-memory-management | MemoryHigh/Max from memory plan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-linger-required, r2-restart-on-failure, r3-environmentfile-not-inline, r4-named-owner, r5-journal-standardoutput | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the systemd User Services artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: no-linger-dies-on-logout, restart-always-spins, inline-environment-leaks, no-memory-bound | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-unit` | sonnet | Per-service template fill with safety checks. |
| `audit-existing-units` | sonnet | Diff against rule-set. |
| `render-timer-pair` | haiku | Mechanical template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/systemd-user-services.json` | UnitPlan JSON skeleton. |
| `templates/systemd-user-services.md.j2` | Human-readable audit trail. |
| `templates/systemd-user-services.md` | Human-readable audit trail. Generated from `templates/systemd-user-services.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/fastapi.service` | Reference unit for a FastAPI app. |
| `templates/celery-worker.service` | Reference unit for a Celery worker. |
| `templates/telegram-bot.service` | Reference unit for a Telegram bot. |
| `templates/target.service` | Reference target grouping multiple units. |
| `templates/timer-pair.service` | Reference .service + .timer pair for periodic jobs. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-systemd-user-services.py` | Validate UnitPlan JSON against the schema. | Pre-install + post-edit. |

## Related

- [[secrets-management]]
- [[swap-memory-management]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/systemd-user-services.json`

```json
{
  "artefact_id": "<svc-name>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "unit_name": "<svc>.service",
  "exec_start": "/path/to/binary --flags",
  "environment_file": "/etc/<svc>.env",
  "restart": "on-failure",
  "memory_high": "1G",
  "memory_max": "2G",
  "linger_enabled": true,
  "owner": "<@handle>"
}
```

### `templates/fastapi.service`

```ini
[Unit]
Description=NERO Channel Web (FastAPI/uvicorn)
After=network-online.target
Wants=network-online.target
StartLimitBurst=5
StartLimitIntervalSec=60

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-channel-web/src
EnvironmentFile=/home/nero/workspace/.env

ExecStart=/srv/nero/nero-channel-web/.venv/bin/uvicorn \
    nero_channel_web.main:app \
    --host 127.0.0.1 \
    --port 8100 \
    --workers 2 \
    --log-level info

Restart=on-failure
RestartSec=5

# Resource limits
MemoryMax=2G
MemoryHigh=1500M
MemorySwapMax=256M
CPUQuota=200%
LimitNOFILE=65536
TasksMax=256

# OOM: protect API gateway from being killed first
OOMScoreAdjust=-300
OOMPolicy=stop

# Security hardening (optional but recommended)
NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=default.target
```

### `templates/celery-worker.service`

```ini
[Unit]
Description=NERO Core (Celery Workers)
After=network-online.target
Wants=network-online.target
StartLimitBurst=5
StartLimitIntervalSec=60

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-core/src
EnvironmentFile=/home/nero/workspace/.env

ExecStart=/srv/nero/nero-core/.venv/bin/celery \
    -A nero_core.celery \
    worker \
    --loglevel=info \
    --concurrency=4 \
    --pool=gevent \
    --max-memory-per-child=512000

Restart=on-failure
RestartSec=5

# Resource limits: LLM responses can be large
MemoryMax=8G
MemoryHigh=6G
MemorySwapMax=512M
CPUQuota=400%
LimitNOFILE=65536
TasksMax=512

# Celery workers are sacrificial (restore after OOM)
OOMScoreAdjust=0
OOMPolicy=stop

NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=default.target
```

### `templates/telegram-bot.service`

```ini
[Unit]
Description=NERO Channel Telegram (aiogram bot)
After=network-online.target
Wants=network-online.target
StartLimitBurst=5
StartLimitIntervalSec=60

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-channel-tg/src
EnvironmentFile=/home/nero/workspace/.env

ExecStart=/srv/nero/nero-channel-tg/.venv/bin/python -m nero_channel_tg.main

Restart=on-failure
RestartSec=5

# Lightweight bot: limited resources
MemoryMax=1G
MemoryHigh=768M
MemorySwapMax=128M
CPUQuota=100%
LimitNOFILE=4096
TasksMax=64

OOMScoreAdjust=-200
OOMPolicy=stop

NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=default.target
```

### `templates/target.service`

```ini
# ~/.config/systemd/user/nero.target
# Target unit: group NERO services so they start/stop together
#
# Usage:
#   systemctl --user enable nero.target    (sets as boot target)
#   systemctl --user start nero.target     (starts all Wants= services)
#   systemctl --user stop nero.target      (stops all Wants= services)
#   systemctl --user restart nero.target   (restarts all)

[Unit]
Description=NERO Platform
# List all services that belong to this platform
Wants=nero-core.service nero-channel-web.service nero-channel-tg.service nero-web.service

[Install]
WantedBy=default.target
```

### `templates/timer-pair.service`

```ini
# Timer unit: schedule the service below
# ~/.config/systemd/user/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
# Run once daily at midnight
OnCalendar=daily

# Run missed execution once after boot (e.g., server was down at midnight)
Persistent=true

# Spread load: random delay up to 5 minutes
RandomizedDelaySec=300

[Install]
WantedBy=timers.target

# ─────────────────────────────────────────────────────────────
# Service unit (save as separate file: backup.service)
# ~/.config/systemd/user/backup.service
# ─────────────────────────────────────────────────────────────
# [Unit]
# Description=Daily backup
#
# [Service]
# Type=oneshot
# WorkingDirectory=/home/nero/workspace
# EnvironmentFile=/home/nero/workspace/.env
# ExecStart=/home/nero/workspace/scripts/backup.sh
# StandardOutput=journal
# StandardError=journal
#
# # No [Install] section needed for timer-activated services

# ─────────────────────────────────────────────────────────────
# Management commands:
#   systemctl --user enable --now backup.timer
#   systemctl --user list-timers
#   systemctl --user status backup.timer
#   journalctl --user -u backup.service    # view run history
```
