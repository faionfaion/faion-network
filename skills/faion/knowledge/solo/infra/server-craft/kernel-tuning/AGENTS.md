---
slug: kernel-tuning
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "sysctl parameter tuning for Ubuntu 24 VPS: inotify ceilings, FD max, network buffer + BBR, vm.swappiness, vm.max_map_count for ES-like workloads, kernel.pid_max for parallel agents."
content_id: "89b5f9b072221b07"
complexity: medium
produces: report
est_tokens: 6000
tags: [kernel, sysctl, performance, inotify, network]
---
# Kernel Tuning (sysctl) for VPS

## Summary

**One-sentence:** sysctl parameter tuning for Ubuntu 24 VPS: inotify ceilings, FD max, network buffer + BBR, vm.swappiness, vm.max_map_count for ES-like workloads, kernel.pid_max for parallel agents.

**One-paragraph:** Distro defaults are conservative for general use; a VPS running modern services hits the ceiling on three categories: file watchers (inotify), network throughput (TCP buffers + BBR), and process density (pid_max + max_map_count). This methodology produces a /etc/sysctl.d/60-vps-tuning.conf drop-in with documented rationale per parameter, verify commands, and a smoke test that confirms each value persists across reboot.

## Applies If (ALL must hold)

- Ubuntu 24 VPS running Docker / agents / DBs.
- Operator can edit /etc/sysctl.d/ with sudo.
- Reboot is acceptable in the maintenance window.

## Skip If (ANY kills it)

- Managed kernel (some PaaS) — sysctl writes ignored.
- Container-only environment — host kernel is shared, tune the host instead.
- Single-purpose embedded device — defaults likely tighter than needed.

**Ефективно для:**

- ENOSPC inotify exhaustion після setup Claude Code.
- Network throughput bottleneck під час backup uploads.
- Elastic-search-like workload з vm.max_map_count помилкою.
- Many-parallel-agent setups з pid_max wall.

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
| `solo/infra/server-craft/agent-dev-tuning` | Sibling — agent-specific subset of these knobs. |
| `solo/infra/server-craft/swap-memory-management` | vm.swappiness lives at this layer. |

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
| `templates/skeleton.md` | Kernel tuning audit report listing keys + rationale + verify. |
| `templates/_smoke-test.md` | Minimum viable filled-in kernel-tuning audit. |
| `templates/60-vps-tuning.conf` | sysctl drop-in for a multi-service VPS with rationale per line. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kernel-tuning.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[agent-dev-tuning]]
- [[swap-memory-management]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
