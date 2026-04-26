# Swap and Memory Management

## Summary

Swap file setup, `vm.swappiness` tuning, OOM killer priority (`oom_score_adj`, `OOMScoreAdjust`), and systemd cgroup memory limits (`MemoryMax`, `MemoryHigh`) for VPS servers running multi-service AI platforms. For a 30GB RAM server: create a 4GB swap file, set swappiness=10, protect databases with `OOMScoreAdjust=-900`, allow Celery workers to be sacrificed at `OOMScoreAdjust=0`.

## Why

Default swappiness=60 causes aggressive paging even when 20GB RAM is free, creating latency spikes during LLM API responses. Without `MemoryMax` in systemd services, a Celery worker processing a large context window can grow unbounded and trigger the kernel OOM killer — which then kills a random process, often the wrong one. Explicit `OOMScoreAdjust` values ensure that if OOM must kill something, it kills the least critical service first.

## When To Use

- New server setup — create swap file and tune swappiness before deploying services
- OOM kills appearing in dmesg/journalctl — set `MemoryMax` and `OOMScoreAdjust` per service
- Server swapping despite available RAM — reduce swappiness
- Planning memory allocation for a multi-service platform
- Celery workers or LLM services have unbounded memory growth

## When NOT To Use

- Managed Kubernetes (memory limits belong in Pod specs, not host sysctl)
- Servers with only 1-2GB RAM where swap is a primary resource (different sizing rules apply)
- When Docker manages the services — set `mem_limit` in compose instead of systemd `MemoryMax`

## Content

| File | What's inside |
|------|---------------|
| `content/01-swap-swappiness.xml` | Swap file creation, sizing guidelines, swappiness values, fstab persistence |
| `content/02-oom-cgroups.xml` | OOM killer scoring, per-service priority table, systemd MemoryMax/MemoryHigh/MemorySwapMax, cgroup monitoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/swap-create.sh` | Idempotent swap file creation and fstab persistence |
| `templates/99-memory.conf` | `/etc/sysctl.d/` drop-in for swappiness and dirty page tuning |
| `templates/nero-core.service.snippet` | systemd service memory limit and OOM policy directives |
| `templates/memory-alert.sh` | Alert when RAM or swap exceeds threshold |
