---
slug: swap-memory-management
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a per-host swap + cgroup memory plan — swappiness, swap size, MemoryHigh/Max per unit, low-memory alert — gated by total-RAM and workload class.
content_id: "64d375e645b86cbd"
complexity: medium
produces: config
est_tokens: 4400
tags: ["swap", "memory", "cgroups", "sysctl", "oom"]
---
# Swap & Memory Management

## Summary

**One-sentence:** Generates a per-host swap + cgroup memory plan — swappiness, swap size, MemoryHigh/Max per unit, low-memory alert — gated by total-RAM and workload class.

**One-paragraph:** On a 4-8GB VPS, OOM-killer evicts your own services if you don't bound them. This methodology pins swap size (2x RAM up to 8GB, capped at 16GB), swappiness (10 for SSD), per-systemd-unit MemoryHigh/Max cgroup limits, and a memory-pressure alert. Output: a MemoryPlan + sysctl 99-memory.conf.

**Ефективно для:**

- VPS with ≤16GB RAM running multiple services (claude, n8n, postgres).
- Boxes that have OOM-killed the wrong process at least once.
- Tmux panes / claude subagents that must not blow up the host.
- Long-running batch jobs that need MemoryHigh throttling.

## Applies If (ALL must hold)

- VPS has ≤16GB RAM AND runs ≥2 memory-hungry services.
- Host has experienced OOM-kill of unrelated services (cascade).
- Adding a new heavyweight workload (LLM inference, large build).
- Auditing existing swap + cgroup posture.

## Skip If (ANY kills it)

- Host has ≥32GB RAM and a single tenant workload.
- Container platform where memory limits are managed by the orchestrator.
- Read-only / serving-only hosts with stable footprint.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Total RAM + free disk | GB | `free -h` + `df -h` |
| Workload class per service | {light, medium, heavy} | operator inventory |
| Alert path | tg-send / email | monitoring config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| systemd-user-services | MemoryHigh/Max live in systemd unit drop-ins. |
| monitoring-logging | Alert path consumed by the memory-pressure trigger. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-swap-size-bounded, r2-swappiness-10-ssd, r3-memoryhigh-per-unit, r4-named-owner, r5-pressure-alert | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Swap & Memory Management artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: no-swap-on-vps, swappiness-60-default, no-cgroup-limits, alert-on-oom-only | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size-swap` | haiku | Lookup table by RAM. |
| `draft-memory-plan` | sonnet | Per-service classification with stakes. |
| `render-drop-ins` | haiku | Mechanical template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/swap-memory-management.json` | MemoryPlan JSON skeleton. |
| `templates/swap-memory-management.md` | Human-readable audit trail. |
| `templates/99-memory.conf` | sysctl drop-in: vm.swappiness=10 + vm.overcommit_memory=1. |
| `templates/swap-create.sh` | Idempotent swapfile creator + fstab entry. |
| `templates/memory-alert.sh` | Pressure-stall-information based alert script. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-swap-memory-management.py` | Validate MemoryPlan JSON against the schema. | Pre-apply + post-incident. |

## Related

- [[systemd-user-services]]
- [[monitoring-logging]]
- [[kernel-tuning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
