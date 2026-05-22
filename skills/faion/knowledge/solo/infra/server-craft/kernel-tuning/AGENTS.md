---
slug: kernel-tuning
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: sysctl parameter tuning for Ubuntu 24.
content_id: "89b5f9b072221b07"
tags: [kernel, sysctl, performance, inotify, network]
---
# Kernel Tuning

## Summary

**One-sentence:** sysctl parameter tuning for Ubuntu 24.

**One-paragraph:** sysctl parameter tuning for Ubuntu 24.04 VPS running web services and AI agent workloads. Four drop-in files under `/etc/sysctl.d/`: network performance (BBR + TCP buffers), agent tuning (inotify watches), memory management (swappiness), and security hardening. Apply with `sudo sysctl --system`. The critical non-obvious rule: inotify `max_user_watches` defaults to 65536 — Claude Code exhausts this on large codebases, causing "No space left on device" errors on file watchers.

## Applies If (ALL must hold)

- New server setup: apply all four sysctl.d files as standard baseline
- Claude Code or file watchers emit "ENOSPC: inotify watches reached" — increase `fs.inotify.max_user_watches`
- Server swaps aggressively despite available RAM — set `vm.swappiness=10`
- WebSocket/API performance is below expectations — enable TCP BBR
- Hardening a production VPS against information leakage

## Skip If (ANY kills it)

- Kubernetes nodes — resource limits are managed at the pod/container level, not via host sysctl
- Shared hosting where root access is not available
- Containers (Docker) — sysctl changes in containers require `--sysctl` flag or privileged mode

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
