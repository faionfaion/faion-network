---
slug: systemd-user-services
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a systemd --user unit + drop-in plan (Restart, MemoryMax, EnvironmentFile, journal) for a long-running solo service — gated by `loginctl enable-linger`.
content_id: "78c891698cd43af9"
complexity: medium
produces: config
est_tokens: 4500
tags: ["systemd", "user-services", "linger", "journal", "drop-in"]
---
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
| `templates/systemd-user-services.md` | Human-readable audit trail. |
| `templates/fastapi.service` | Reference unit for a FastAPI app. |
| `templates/celery-worker.service` | Reference unit for a Celery worker. |
| `templates/telegram-bot.service` | Reference unit for a Telegram bot. |
| `templates/target.service` | Reference target grouping multiple units. |
| `templates/timer-pair.service` | Reference .service + .timer pair for periodic jobs. |

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
