# Agent Integration — Kernel Tuning

## When to use
- New VPS provisioning: apply tuning before deploying any services
- Claude Code or other file-watcher tools report "too many open files" or inotify errors
- TCP throughput is poor on a server handling WebSocket or long-lived API connections
- OOM kills are occurring despite adequate total RAM (often a swappiness/overcommit issue)
- Docker or database workloads fail with `vm.max_map_count` errors (e.g., Elasticsearch, Qdrant)
- Post-kernel-upgrade validation: confirm custom sysctl settings survived the update

## When NOT to use
- Managed hosting (Heroku, Render, Railway) where sysctl access is unavailable
- Kubernetes pods — sysctl tuning is set at the node level or via `securityContext.sysctls`; pod-level is restricted
- Settings that require kernel module (e.g., BBR needs `tcp_bbr` module loaded); verify with `lsmod | grep bbr` first
- Changing `vm.overcommit_memory=2` on a production server without load-testing first — can cause legitimate allocations to fail

## Where it fails / limitations
- `sysctl --system` applies all drop-in files but does not persist across config errors; a typo in one file blocks all files processed after it alphabetically
- BBR requires both `net.core.default_qdisc = fq` AND `net.ipv4.tcp_congestion_control = bbr`; setting only one has no effect
- `fs.inotify.max_user_watches` is per-user, not global; raising it does not help processes running as other users (e.g., www-data)
- `net.netfilter.nf_conntrack_max` requires the `nf_conntrack` module to be loaded; the setting silently has no effect otherwise
- Changes to `/etc/fstab` for `noatime` require remount or reboot; agents must not assume the flag is active after editing the file only

## Agentic workflow
A provisioning agent reads the target server specs (RAM, CPU, expected workloads) and generates a `/etc/sysctl.d/99-custom.conf` with settings appropriate for those workloads. It then applies the config with `sudo sysctl --system` and runs verification commands (`sysctl net.ipv4.tcp_congestion_control`, `cat /proc/sys/fs/inotify/max_user_watches`) to confirm each setting took effect. Results are logged before and after so the human can review the delta. The agent must not modify existing system-provided files in `/etc/sysctl.d/` — only write to `99-custom.conf`.

### Recommended subagents
- `faion` (infra/server-craft/swap-memory-management) — pairs with `vm.swappiness` and OOM tuning
- `faion` (infra/server-craft/agent-dev-tuning) — inotify and file descriptor tuning for Claude Code workloads
- `faion` (infra/server-craft/server-init-bootstrap) — kernel tuning is step 2 in bootstrap sequence

### Prompt pattern
```
Apply kernel tuning for a 30GB RAM Ubuntu 24.04 server running:
- Python API services (FastAPI, Celery)
- Claude Code agent sessions
- Docker containers (Postgres, Redis)

Generate /etc/sysctl.d/99-custom.conf with settings for: BBR + fq, TCP buffers, inotify watches,
vm.swappiness=10, vm.max_map_count=1048576, file descriptor limits.
Then: sudo sysctl --system
Verify each setting with sysctl <key>. Report any that did not apply.
```

```
Check current inotify usage on this server:
find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | cut -d/ -f3 | \
  xargs -I{} sh -c 'cat /proc/{}/cmdline 2>/dev/null | tr "\0" " "; echo ""' | \
  sort | uniq -c | sort -rn | head -10
Compare with: cat /proc/sys/fs/inotify/max_user_watches
If usage > 80% of max, increase max_user_watches to 524288.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sysctl` | Read/write kernel parameters | Pre-installed (procps) |
| `sysctl --system` | Apply all sysctl.d drop-in files | procps |
| `sysctl -p <file>` | Apply a specific config file | procps |
| `lsmod` | List loaded kernel modules | kmod (pre-installed) |
| `modprobe tcp_bbr` | Load BBR congestion control module | kmod |
| `ss -s` | Socket statistics (connection counts) | iproute2 (pre-installed) |
| `cat /proc/net/sockstat` | TCP memory usage | procfs |
| `conntrack -C` | Count active connection tracking entries | `apt install conntrack` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ubuntu sysctl.d | OSS (kernel) | Yes (file write + CLI) | Drop-in config in `/etc/sysctl.d/`; apply with `sysctl --system` |
| Ansible | OSS | Yes | `sysctl` module for idempotent kernel tuning across multiple hosts |
| Lynis | OSS | Yes (CLI) | Security audit; flags missing kernel hardening settings |
| `procps` | OSS | Yes | `sysctl` binary; pre-installed on Ubuntu |

## Templates & scripts
See `templates.md` for full sysctl config templates. Inline verification script:

```bash
#!/bin/bash
# verify-kernel-tuning.sh — check that key sysctl settings are applied
set -euo pipefail
PASS=0; FAIL=0
check() {
  local key="$1" expected="$2"
  local actual; actual=$(sysctl -n "$key" 2>/dev/null || echo "MISSING")
  if echo "$actual" | grep -q "$expected"; then
    echo "OK  $key = $actual"
    ((PASS++))
  else
    echo "FAIL $key: expected '$expected', got '$actual'"
    ((FAIL++))
  fi
}
check net.ipv4.tcp_congestion_control bbr
check net.core.default_qdisc fq
check fs.inotify.max_user_watches 524288
check vm.swappiness 10
check vm.max_map_count 1048576
check net.core.somaxconn 65535
echo "---"
echo "Passed: $PASS | Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
```

## Best practices
- Always write custom settings to `/etc/sysctl.d/99-custom.conf` (highest priority) rather than editing system-provided files; this survives package upgrades
- Verify BBR is actually active after applying — kernel may silently fall back to Cubic if the `tcp_bbr` module is not loaded; check with `sysctl net.ipv4.tcp_congestion_control`
- Scale TCP buffer sizes to available RAM; setting 16MB buffers on a 2GB VPS will exhaust socket memory under load
- Do not set `vm.swappiness=0` — this causes OOM kills when memory is momentarily exhausted rather than using available swap; `10` is the correct value for latency-sensitive workloads
- After editing `/etc/fstab` to add `noatime`, run `sudo mount -o remount,noatime /` to activate without reboot; verify with `findmnt -o OPTIONS /`
- Combine inotify watch increase with `LimitNOFILE` in systemd unit files — raising watches without raising file descriptors often hits the file descriptor limit first

## AI-agent gotchas
- Agents must not modify files in `/etc/sysctl.d/` that begin with `10-` (system-provided); write only to `99-custom.conf`
- `sysctl --system` output can be very long; agents should pipe to `grep -E "(Error|fail|custom)"` to surface only relevant lines
- A setting applied via `sysctl -w key=value` is not persistent; agents must write to the config file AND apply with `sysctl --system`
- Some parameters (e.g., `net.netfilter.nf_conntrack_max`) return "No such file or directory" if the kernel module is not loaded; agents must handle this as "module not loaded", not as a kernel bug
- Agents must always run the verification script after applying — sysctl silently ignores unknown keys on some kernel versions without returning an error

## References
- https://www.kernel.org/doc/Documentation/sysctl/
- https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster
- https://man7.org/linux/man-pages/man7/inotify.7.html
- https://fasterdata.es.net/host-tuning/linux/
- https://wiki.ubuntu.com/Security/Features
