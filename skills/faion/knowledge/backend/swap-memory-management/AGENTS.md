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
| `templates/swap-memory-management.md.j2` | Human-readable audit trail. |
| `templates/swap-memory-management.md` | Human-readable audit trail. Generated from `templates/swap-memory-management.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/99-memory.conf` | sysctl drop-in: vm.swappiness=10 + vm.overcommit_memory=1. |
| `templates/swap-create.sh` | Idempotent swapfile creator + fstab entry. |
| `templates/memory-alert.sh` | Pressure-stall-information based alert script. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/swap-memory-management.json`

```json
{
  "artefact_id": "memory-<host>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "ram_gb": 8,
  "swap_gb": 16,
  "swappiness": 10,
  "units": [
    {
      "unit": "<svc>.service",
      "MemoryHigh": "<size>",
      "MemoryMax": "<size>"
    }
  ],
  "alert_path": "tg-send admin",
  "owner": "<@handle>"
}
```

### `templates/99-memory.conf`

```conf
# /etc/sysctl.d/99-memory.conf
# Memory management for servers with 16GB+ RAM running AI/web workloads
# Apply: sudo sysctl --system

# Low swappiness: prefer RAM, only swap under real pressure
# Never set to 0 — that disables the swap safety net
vm.swappiness = 10

# Dirty page writeback: avoid I/O spikes
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5

# Cache pressure: keep inode/dentry caches longer
vm.vfs_cache_pressure = 50

# Max memory map areas: required by JVM, Elasticsearch, some ML libs
vm.max_map_count = 1048576

# Overcommit: heuristic (safe default; do NOT set to 1 on production)
vm.overcommit_memory = 0
```

### `templates/swap-create.sh`

```bash
# swap-create.sh — Idempotent swap file creation and fstab persistence
# Usage: sudo bash swap-create.sh [size]
#   size: e.g. 4G (default), 8G, 2G
set -euo pipefail

SIZE="${1:-4G}"
SWAPFILE="/swapfile"

# Already configured?
if swapon --show | grep -q "$SWAPFILE"; then
    echo "[OK] Swap already active: $(swapon --show | grep "$SWAPFILE")"
    exit 0
fi

if [[ -f "$SWAPFILE" ]]; then
    echo "[INFO] $SWAPFILE exists but is not active; re-enabling..."
    chmod 600 "$SWAPFILE"
    mkswap "$SWAPFILE"
    swapon "$SWAPFILE"
else
    echo "[CREATE] Allocating $SIZE swap at $SWAPFILE..."
    fallocate -l "$SIZE" "$SWAPFILE"
    chmod 600 "$SWAPFILE"
    mkswap "$SWAPFILE"
    swapon "$SWAPFILE"
fi

# fstab persistence (idempotent)
if ! grep -q "$SWAPFILE" /etc/fstab; then
    echo "$SWAPFILE none swap sw 0 0" >> /etc/fstab
    echo "[OK] Added $SWAPFILE to /etc/fstab"
fi

# Verify fstab syntax (broken entry can prevent boot)
findmnt --verify && echo "[OK] fstab syntax valid" || { echo "[ERROR] fstab invalid — fix before reboot!"; exit 1; }

echo "[DONE] Swap:"
swapon --show
free -h | grep Swap
```

### `templates/memory-alert.sh`

```bash
# memory-alert.sh — Alert when RAM or swap exceeds threshold
# Usage: bash memory-alert.sh [ram_threshold] [swap_threshold]
#   Defaults: RAM 90%, Swap 50%
# Suitable for cron: */5 * * * * bash ~/workspace/scripts/memory-alert.sh
set -euo pipefail

RAM_THRESHOLD="${1:-90}"
SWAP_THRESHOLD="${2:-50}"

ram_pct=$(free | awk '/^Mem:/{printf "%.0f", $3/$2 * 100}')
swap_total=$(free | awk '/^Swap:/{print $2}')
if [[ "$swap_total" -gt 0 ]]; then
    swap_pct=$(free | awk '/^Swap:/{printf "%.0f", $3/$2 * 100}')
else
    swap_pct=0
fi

alert=false

if [[ "$ram_pct" -gt "$RAM_THRESHOLD" ]]; then
    echo "ALERT: RAM usage at ${ram_pct}% (threshold: ${RAM_THRESHOLD}%)"
    alert=true
fi

if [[ "$swap_pct" -gt "$SWAP_THRESHOLD" ]]; then
    echo "ALERT: Swap usage at ${swap_pct}% (threshold: ${SWAP_THRESHOLD}%)"
    alert=true
fi

if [[ "$alert" == "true" ]]; then
    echo ""
    echo "Top memory consumers:"
    ps aux --sort=-%mem --no-headers | head -8 | awk '{printf "  %-20s %5s%% %s\n", $1, $4, $11}'

    echo ""
    echo "Swap usage by process:"
    for f in /proc/[0-9]*/status; do
        awk '/VmSwap|Name/{printf $2 " " $3}END{print ""}' "$f" 2>/dev/null
    done | sort -k2 -rn | head -5

    # Optionally notify via Telegram (requires tg-send in PATH)
    if command -v tg-send &>/dev/null; then
        tg-send "Memory alert on $(hostname): RAM=${ram_pct}%, Swap=${swap_pct}%"
    fi
    exit 1
fi

echo "OK: RAM=${ram_pct}%, Swap=${swap_pct}%"
```
