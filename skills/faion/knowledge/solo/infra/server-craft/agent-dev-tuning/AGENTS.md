---
slug: agent-dev-tuning
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Server-side tuning for AI agent workloads on a Linux VPS: inotify ceilings, PAM nofile, 4-8GB swap with swappiness=10, per-agent MemoryMax via systemd-run, tmux linger, git worktrees for parallelism."
content_id: "25e2b385ea3751ac"
complexity: medium
produces: report
est_tokens: 6000
tags: [agent-dev, inotify, swap, tmux, worktree]
---
# Agent Dev Tuning for VPS

## Summary

**One-sentence:** Server-side tuning for AI agent workloads on a Linux VPS: inotify ceilings, PAM nofile, 4-8GB swap with swappiness=10, per-agent MemoryMax via systemd-run, tmux linger, git worktrees for parallelism.

**One-paragraph:** Defaults break silently under agent workloads: inotify exhaustion surfaces as 'ENOSPC' that looks like disk-full; missing swap causes OOM kills during LLM response processing; agents started in bare SSH die on disconnect; two agents on the same branch overwrite each other. This methodology fixes them at the OS / config layer once with a verifiable artefact: every step has a verify_cmd, every cmd has an expected output, every change persists across reboot.

## Applies If (ALL must hold)

- Linux VPS running Claude Code or similar agent workloads.
- Seeing 'ENOSPC: System limit for number of file watchers reached' OR agent OOM kills.
- Running >1 parallel agent on the same repository.

## Skip If (ANY kills it)

- Local macOS/Windows development — inotify is Linux-specific.
- Cloud-managed AI platforms (Codespaces, Replit) manage the environment.
- Single short-lived agent session — tuning overhead not worth it.

**Ефективно для:**

- Self-hosted Claude Code на Hetzner / OVH / DigitalOcean VPS.
- Команди де 2-3 агенти працюють паралельно через git worktree.
- VPS з 16-32GB RAM де OOM-kill під час LLM-response — щоденна проблема.
- Tmux-користувачі що втрачають session при SSH-disconnect.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/kernel-tuning` | sysctl drop-in patterns. |
| `solo/infra/server-craft/swap-memory-management` | Swap allocation procedure. |
| `solo/infra/server-craft/tmux-power-user` | tmux session shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown report listing applied tuning + verify commands. |
| `templates/_smoke-test.md` | Minimum viable filled-in tuning report. |
| `templates/60-agent-dev.conf` | sysctl drop-in for agent workloads (inotify + memory + FD). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-dev-tuning.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[kernel-tuning]]
- [[swap-memory-management]]
- [[tmux-power-user]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
