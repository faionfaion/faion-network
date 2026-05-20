---
slug: agent-dev-tuning
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Server-side tuning checklist for running Claude Code and other AI agents on a VPS: raise inotify max_user_watches to 524288, configure PAM file descriptor limits, add 4-8GB swap with swappiness=10, set per-agent MemoryMax via systemd-run or cgroup scopes, use tmux with linger for session persistence, and use git worktrees for parallel agent execution without branch conflicts.
content_id: "25e2b385ea3751ac"
tags: [agent-dev, inotify, swap, tmux, worktree]
---
# Agent Dev Tuning for VPS Infrastructure

## Summary

**One-sentence:** Server-side tuning checklist for running Claude Code and other AI agents on a VPS: raise inotify max_user_watches to 524288, configure PAM file descriptor limits, add 4-8GB swap with swappiness=10, set per-agent MemoryMax via systemd-run or cgroup scopes, use tmux with linger for session persistence, and use git worktrees for parallel agent execution without branch conflicts.

**One-paragraph:** Server-side tuning checklist for running Claude Code and other AI agents on a VPS: raise inotify max_user_watches to 524288, configure PAM file descriptor limits, add 4-8GB swap with swappiness=10, set per-agent MemoryMax via systemd-run or cgroup scopes, use tmux with linger for session persistence, and use git worktrees for parallel agent execution without branch conflicts.

## Applies If (ALL must hold)

- Setting up a new VPS for Claude Code agent work
- Seeing "ENOSPC: System limit for number of file watchers reached" errors
- Agent sessions dying when SSH disconnects
- Running multiple parallel agents on the same repository
- OOM kills during LLM API calls or large context processing

## Skip If (ANY kills it)

- Local macOS/Windows development — inotify is Linux-specific; macOS uses FSEvents
- Cloud-managed AI platforms (Replit, Codespaces) — these manage the environment for you
- Single short-lived agent sessions where full tuning is not worth the overhead

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
