# Agent Dev Tuning

## Summary

Server-side tuning checklist for running Claude Code and other AI agents on a VPS: raise inotify `max_user_watches` to 524288, configure PAM file descriptor limits, add 4-8GB swap with swappiness=10, set per-agent `MemoryMax` via systemd-run or cgroup scopes, use tmux with linger for session persistence, and use git worktrees for parallel agent execution without branch conflicts.

## Why

Defaults break silently under agent workloads: inotify exhaustion (8192 default watches vs 50k+ consumed by Claude Code on a large workspace) surfaces as "ENOSPC" errors that look like disk-full; missing swap causes OOM kills during LLM response processing; agents started in bare SSH sessions die on disconnect; two agents on the same branch overwrite each other's changes. These are infrastructure problems, not code problems — fix them at the OS/config layer once.

## When To Use

- Setting up a new VPS for Claude Code agent work
- Seeing "ENOSPC: System limit for number of file watchers reached" errors
- Agent sessions dying when SSH disconnects
- Running multiple parallel agents on the same repository
- OOM kills during LLM API calls or large context processing

## When NOT To Use

- Local macOS/Windows development — inotify is Linux-specific; macOS uses FSEvents
- Cloud-managed AI platforms (Replit, Codespaces) — these manage the environment for you
- Single short-lived agent sessions where full tuning is not worth the overhead

## Content

| File | What's inside |
|------|---------------|
| `content/01-kernel-limits.xml` | inotify tuning, PAM nofile/nproc, swappiness, filesystem noatime |
| `content/02-agent-patterns.xml` | tmux session setup with linger, git worktree workflow for parallel agents, resource-limited agent launcher, pre-flight check script |

## Templates

| File | Purpose |
|------|---------|
| `templates/60-agent-dev.conf` | sysctl drop-in: inotify + memory + file descriptors |
| `templates/nero-agent.limits.conf` | PAM limits for agent user |
| `templates/claude-settings.json` | Claude Code settings.json with common allow list |
| `templates/agent-session.sh` | tmux session setup: work + logs + monitor windows |
| `templates/worktree.sh` | Git worktree create/list/remove/clean management |
| `templates/verify-agent-tuning.sh` | Verify all tuning is applied, print OK/LOW per item |
