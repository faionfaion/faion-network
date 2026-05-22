---
slug: tmux-power-user
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Master tmux for remote development: configure prefix (Ctrl+A), enable mouse and vi-mode, set up intuitive pane/window navigation, install plugins (resurrect/continuum) for session persistence, customize the status bar with system metrics, and build session templates for parallel project workflows.
content_id: "7ca36d875cb179f1"
tags: [tmux, terminal, multiplexing, session-management, remote-work]
---
# tmux Power User

## Summary

**One-sentence:** Master tmux for remote development: configure prefix (Ctrl+A), enable mouse and vi-mode, set up intuitive pane/window navigation, install plugins (resurrect/continuum) for session persistence, customize the status bar with system metrics, and build session templates for parallel project workflows.

**One-paragraph:** Master tmux for remote development: configure prefix (Ctrl+A), enable mouse and vi-mode, set up intuitive pane/window navigation, install plugins (resurrect/continuum) for session persistence, customize the status bar with system metrics, and build session templates for parallel project workflows.

## Applies If (ALL must hold)

- Developer works primarily over SSH and needs persistent sessions
- Running multiple concurrent AI agent sessions that must stay live without supervision
- Building a named-session workflow where each project has a dedicated tmux session
- Setting up a monitoring dashboard with persistent panes (htop, logs, docker stats)
- Scripting session layouts that an agent or cron job can create/restore

## Skip If (ANY kills it)

- Local-only workstation development where an IDE terminal suffices
- Ephemeral CI/CD environments (tmux adds no value in non-interactive pipelines)
- Containerized deployments where the process is PID 1
- Terminals that do not support 256-color or proper escape sequences

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
