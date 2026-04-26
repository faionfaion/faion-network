# tmux Power User

## Summary

Comprehensive tmux configuration and workflow for developers managing multiple projects and AI agent sessions on remote servers. Covers prefix customization (Ctrl+A), mouse/vi-mode, pane/window navigation, TPM plugin management (resurrect, continuum), status bar with system metrics, and session templates for project layouts.

## Why

For a solo developer on a remote server, tmux is the foundation of productivity: sessions survive SSH disconnections, multiple panes enable simultaneous log-watching and code editing, and plugins (resurrect/continuum) auto-save/restore sessions across reboots. Without it, every reconnect means rebuilding context from scratch.

## When To Use

- Developer works primarily over SSH and needs persistent sessions
- Running multiple concurrent AI agent sessions that must stay live without supervision
- Building a named-session workflow where each project has a dedicated tmux session
- Setting up a monitoring dashboard with persistent panes (htop, logs, docker stats)
- Scripting session layouts that an agent or cron job can create/restore

## When NOT To Use

- Local-only workstation development where an IDE terminal suffices
- Ephemeral CI/CD environments (tmux adds no value in non-interactive pipelines)
- Containerized deployments where the process is PID 1
- Terminals that do not support 256-color or proper escape sequences

## Content

| File | What's inside |
|------|---------------|
| `content/01-config.xml` | Prefix key, mouse support, vi copy-mode, split/navigation bindings, status bar setup |
| `content/02-plugins.xml` | TPM installation, resurrect/continuum/yank configuration, gotchas |
| `content/03-sessions.xml` | Session commands, session templates, nested tmux pattern, agent-control via send-keys/capture-pane |

## Templates

| File | Purpose |
|------|---------|
| `templates/tmux.conf` | Complete power-user .tmux.conf with all settings and TPM plugins |
| `templates/tmux-system.sh` | Status bar script: CPU/MEM/Disk with color-coded thresholds |
| `templates/tmux-session.sh` | Generic create-or-attach session launcher (agent-safe) |
