# Agent Integration — Swap and Memory Management

## When to use
- New VPS provisioning with no swap configured — always set up swap before deploying services
- OOM kills appearing in `journalctl -k --grep=OOM` on a server with seemingly available RAM
- Celery workers or LLM-calling processes consuming unpredictable RAM (large context windows cause spikes)
- Setting per-service memory ceilings to protect critical services from being starved by runaway workers
- Server RAM > 16GB and swap is still at 0 — add a small swap as an OOM safety net

## When NOT to use
- Containers managed by Kubernetes with resource requests/limits set — container-level MemoryMax takes precedence; swap on the node may interfere
- Read-only filesystems or ephemeral instances (cloud spot instances with no persistent disk)
- NFS-mounted runtime directories — swapfile on NFS is unsupported and will fail
- Database servers where swap-induced latency is unacceptable — set `vm.swappiness=0` and eliminate swap entirely for pure DB servers

## Where it fails / limitations
- `fallocate` fails on filesystems that do not support it (e.g., XFS with reflinks enabled) — use `dd` as fallback
- A broken `/etc/fstab` entry for swapfile prevents boot; always run `sudo findmnt --verify` after editing fstab
- `MemoryMax` in systemd kills the process with SIGKILL when exceeded — no graceful shutdown; set headroom above peak observed usage
- `OOMScoreAdjust=-1000` disables OOM killing entirely for a process; if that process leaks memory it will trigger system-wide OOM instead of being killed itself
- `vm.swappiness=10` does not prevent swapping entirely; under enough memory pressure the kernel will still swap; only `vm.swappiness=0` approaches no-swap (but can trigger premature OOM)
- cgroup v2 memory stats in `/sys/fs/cgroup` paths use user UID in the path; agents must substitute `$(id -u)` correctly or the path will not exist

## Agentic workflow
A provisioning agent checks `free -h` and `swapon --show` on a new server; if swap is absent, it creates a 4GB swapfile, sets `vm.swappiness=10` persistently, and verifies with `swapon --show`. A monitoring agent runs a nightly `memory-alert.sh` check and posts to Telegram if usage exceeds 85%. When a service is added to the platform, an agent reads its expected peak memory from the service manifest and adds `MemoryMax` and `MemoryHigh` directives to the systemd unit file, then reloads the daemon. Human review is required before setting `OOMScoreAdjust` values — getting these wrong can cause the wrong service to be killed in an OOM event.

### Recommended subagents
- `faion-knowledge` (infra/server-craft/kernel-tuning) — `vm.swappiness`, `vm.overcommit_memory` are set via sysctl
- `faion-knowledge` (infra/server-craft/systemd-user-services) — `MemoryMax`, `MemoryHigh`, `OOMScoreAdjust` in unit files
- `faion-knowledge` (infra/server-craft/health-checks-autoheal) — memory pressure alerts feed into autoheal decisions

### Prompt pattern
```
Check swap and memory on this server:
1. free -h
2. swapon --show
3. cat /proc/sys/vm/swappiness

If no swap exists, create 4GB swapfile:
  sudo fallocate -l 4G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  sudo findmnt --verify

Set swappiness to 10 persistently:
  echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swap.conf
  sudo sysctl -p /etc/sysctl.d/99-swap.conf

Verify: swapon --show && sysctl vm.swappiness
```

```
Add systemd memory limits to the nero-core service unit file:
MemoryMax=8G
MemoryHigh=6G
MemorySwapMax=1G
OOMScoreAdjust=0
OOMPolicy=stop

After editing: systemctl --user daemon-reload && systemctl --user restart nero-core
Verify: systemctl --user status nero-core
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fallocate -l` | Fast swapfile creation | util-linux (pre-installed) |
| `mkswap` | Format file as swap | util-linux |
| `swapon` / `swapoff` | Enable/disable swap | util-linux |
| `free -h` | Human-readable memory overview | procps |
| `sysctl vm.swappiness` | Read/set swappiness | procps |
| `findmnt --verify` | Validate fstab after editing | util-linux |
| `systemd-cgtop` | Real-time cgroup memory/CPU stats | systemd |
| `ps aux --sort=-%mem` | Processes sorted by memory usage | procps |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| systemd cgroups v2 | OSS | Yes (unit file directives) | `MemoryMax`, `MemoryHigh` control per-service limits |
| Netdata | OSS | Yes (REST API) | Memory pressure dashboards, OOM event alerts |
| Prometheus + node_exporter | OSS | Yes (REST API) | `node_memory_*` metrics for alerting on memory pressure |
| earlyoom | OSS | Yes (CLI) | Userspace OOM daemon that kills processes before kernel OOM triggers; faster and more configurable |

## Templates & scripts
See `templates.md` for full provisioning scripts. Inline memory alert:

```bash
#!/bin/bash
# memory-alert.sh — alert when memory + swap usage exceeds threshold
THRESHOLD=85
MEM_TOTAL=$(awk '/MemTotal/{print $2}' /proc/meminfo)
MEM_AVAIL=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
SWAP_TOTAL=$(awk '/SwapTotal/{print $2}' /proc/meminfo)
SWAP_FREE=$(awk '/SwapFree/{print $2}' /proc/meminfo)
MEM_PCT=$(( (MEM_TOTAL - MEM_AVAIL) * 100 / MEM_TOTAL ))
SWAP_USED=$((SWAP_TOTAL - SWAP_FREE))
SWAP_PCT=$(( SWAP_TOTAL > 0 ? SWAP_USED * 100 / SWAP_TOTAL : 0 ))
if [ "$MEM_PCT" -gt "$THRESHOLD" ] || [ "$SWAP_PCT" -gt 50 ]; then
  echo "ALERT: RAM ${MEM_PCT}% | SWAP ${SWAP_PCT}%"
  echo "Top consumers:"
  ps aux --sort=-%mem | awk 'NR<=6{printf "%-20s %5s %5s\n", $11, $3, $4}'
fi
```

## Best practices
- Size swap as a safety net, not a performance resource: 4GB is correct for a 30GB RAM server; swapping gigabytes of LLM context to disk causes timeouts
- Run `sudo findmnt --verify` every time `/etc/fstab` is modified — a typo in the swap entry can prevent boot
- Set `OOMScoreAdjust` values on all services before an OOM event; deciding priorities under pressure is too late
- Monitor `SWAP_PCT > 50%` as an alert threshold — sustained swap usage at 50% indicates the server is undersized or has a memory leak
- Use `earlyoom` on servers with memory-intensive AI workloads — it triggers before the kernel OOM killer and avoids the system freeze that often precedes kernel OOM
- Never set `MemoryMax` below the service's peak observed RSS — use `systemd-cgtop` to observe actual peak usage first, then set limit 20-30% above peak

## AI-agent gotchas
- Agents must run `sudo findmnt --verify` after any fstab edit — failing to do so can result in an unbootable server that requires console access to fix
- `fallocate` fails silently on some filesystems; agents must check the exit code and fall back to `dd if=/dev/zero of=/swapfile bs=1M count=4096` if fallocate returns non-zero
- `MemoryMax` in systemd unit files is in bytes unless a unit suffix is given (M, G); agents must always include the unit suffix
- Setting `OOMScoreAdjust=-1000` is effectively disabling OOM protection for the entire system if applied to the wrong process — agents must never set this value without explicit human confirmation
- cgroup memory stats paths include the user's UID (`user-$(id -u)`); agents must evaluate `$(id -u)` at runtime, not hardcode a UID

## References
- https://www.kernel.org/doc/Documentation/sysctl/vm.txt
- https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html
- https://man7.org/linux/man-pages/man5/proc.5.html
- https://github.com/rfjakob/earlyoom
- https://wiki.archlinux.org/title/Swap
