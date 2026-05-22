---
slug: swap-memory-management
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure swap files, tune vm.
content_id: "fa22228c203f3d69"
tags: [swap, memory, oom, systemd, cgroups]
---
# Swap and Memory Management

## Summary

**One-sentence:** Configure swap files, tune vm.

**One-paragraph:** Configure swap files, tune vm.swappiness, set OOM killer priorities, and apply systemd cgroup memory limits to prevent unbounded growth and ensure predictable failure modes on memory-constrained servers.

## Applies If (ALL must hold)

- New server setup — create swap file and tune swappiness before deploying services
- OOM kills appearing in dmesg/journalctl — set MemoryMax and OOMScoreAdjust per service
- Server swapping despite available RAM — reduce swappiness
- Planning memory allocation for a multi-service platform
- Celery workers or LLM services have unbounded memory growth

## Skip If (ANY kills it)

- Managed Kubernetes (memory limits belong in Pod specs, not host sysctl)
- Servers with only 1-2GB RAM where swap is a primary resource (different sizing rules apply)
- When Docker manages the services — set mem_limit in compose instead of systemd MemoryMax

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
