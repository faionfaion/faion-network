# Kernel Tuning

Comprehensive kernel parameter tuning methodology for Ubuntu/Debian VPS servers running AI agent workloads. Covers TCP performance, security hardening, memory management, and filesystem tuning via sysctl.

## Scope

- sysctl.d configuration structure and best practices
- TCP congestion control (BBR)
- TCP buffer tuning for high-throughput workloads
- inotify watches (critical for AI agents and file watchers)
- Memory management (vm.swappiness, overcommit, OOM)
- Security hardening (kptr_restrict, ptrace_scope, ASLR)
- Network security (SYN cookies, ICMP, redirects)
- File descriptor limits
- Queueing discipline (fq_codel, fq)

## Why This Matters

Default kernel parameters are conservative and optimized for general-purpose use. A VPS running:

- **AI agent platform** needs high inotify watches (Claude Code, file watchers)
- **Web services** need optimized TCP stack for WebSocket and HTTP connections
- **Message queues** (RabbitMQ) need tuned network buffers and file descriptors
- **Docker workloads** need memory management tuning to avoid OOM kills

## Architecture

Ubuntu 24.04 sysctl configuration hierarchy:

```
/etc/sysctl.conf                     # Legacy main config (still works)
/etc/sysctl.d/                       # Drop-in directory (recommended)
  10-console-messages.conf           # Console logging level
  10-ipv6-privacy.conf              # IPv6 privacy extensions
  10-kernel-hardening.conf          # Kernel security settings
  10-magic-sysrq.conf              # SysRq key settings
  10-map-count.conf                 # vm.max_map_count
  10-network-security.conf         # Network security (rp_filter)
  10-ptrace.conf                   # PTRACE scope
  10-zeropage.conf                 # vm.mmap_min_addr
  99-sysctl.conf                   # /etc/sysctl.conf symlink
```

Files are processed in alphabetical order. Higher numbers override lower. Use `99-custom.conf` for custom settings to ensure they take priority.

## Key Concepts

### 1. TCP BBR (Bottleneck Bandwidth and RTT)

BBR is Google's TCP congestion control algorithm. It significantly improves throughput and reduces latency compared to the default Cubic, especially on:

- High-latency connections (transatlantic, cloud-to-cloud)
- Networks with packet loss
- Long-lived connections (WebSocket, API)

```bash
# Enable BBR
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
```

Why `fq` instead of `fq_codel`: BBR works best with the `fq` (Fair Queue) qdisc. Ubuntu defaults to `fq_codel`, which is good for bufferbloat but not optimal for BBR's pacing.

### 2. TCP Buffer Tuning

TCP buffer sizes control how much data can be in-flight. Default values are conservative:

| Parameter | Default | Recommended (30GB RAM) | Purpose |
|-----------|---------|----------------------|---------|
| `net.core.rmem_max` | 212992 | 16777216 | Max receive buffer |
| `net.core.wmem_max` | 212992 | 16777216 | Max send buffer |
| `net.ipv4.tcp_rmem` | 4096 131072 6291456 | 4096 87380 16777216 | TCP receive (min, default, max) |
| `net.ipv4.tcp_wmem` | 4096 16384 4194304 | 4096 65536 16777216 | TCP send (min, default, max) |
| `net.core.somaxconn` | 4096 | 65535 | Max listen() backlog |
| `net.core.netdev_max_backlog` | 1000 | 5000 | Max packets queued on input |

### 3. inotify Watches

inotify watches are consumed by file monitoring tools. Default limits are often too low for development:

| Consumer | Typical Usage |
|----------|--------------|
| Claude Code | 5000-50000 watches per workspace |
| VS Code | 10000-50000 watches |
| Docker | 1000-5000 watches per container |
| systemd | 100-500 watches |
| File sync (rsync) | Varies |

```bash
# Default: 65536, Recommended for AI agent workloads
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.inotify.max_queued_events = 32768
```

### 4. Memory Management

| Parameter | Default | Recommended | Purpose |
|-----------|---------|-------------|---------|
| `vm.swappiness` | 60 | 10 | How aggressively kernel swaps (lower = prefer RAM) |
| `vm.dirty_ratio` | 20 | 15 | % of RAM for dirty pages before sync |
| `vm.dirty_background_ratio` | 10 | 5 | % of RAM before background writeback starts |
| `vm.overcommit_memory` | 0 | 0 | 0=heuristic, 1=always allow, 2=strict |
| `vm.max_map_count` | 65530 | 1048576 | Max memory map areas (needed by many apps) |
| `vm.vfs_cache_pressure` | 100 | 50 | How aggressively to reclaim inode/dentry caches |

**vm.swappiness=10:** On a 30GB RAM server running web services and AI agents, memory is abundant. Setting swappiness to 10 keeps applications in RAM and only swaps under heavy memory pressure.

### 5. Security Hardening

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `kernel.kptr_restrict` | 1 | Hide kernel addresses from non-root |
| `kernel.yama.ptrace_scope` | 1 | Restrict ptrace to direct children |
| `kernel.dmesg_restrict` | 1 | Restrict dmesg to root |
| `kernel.randomize_va_space` | 2 | Full ASLR (default, ensure it stays) |
| `kernel.sysrq` | 176 | Limit SysRq to sync+remount+reboot |
| `net.ipv4.tcp_syncookies` | 1 | SYN flood protection |
| `net.ipv4.conf.all.accept_redirects` | 0 | Ignore ICMP redirects |
| `net.ipv4.conf.all.send_redirects` | 0 | Don't send ICMP redirects |
| `net.ipv4.conf.all.rp_filter` | 2 | Loose reverse path filtering |
| `net.ipv4.conf.all.log_martians` | 1 | Log packets with impossible addresses |
| `net.ipv6.conf.all.accept_redirects` | 0 | Ignore IPv6 ICMP redirects |

### 6. File Descriptors

The kernel-level max is controlled by `fs.file-max`. Per-process limits are set via `ulimit`/`pam_limits`:

```bash
# Kernel max (rarely needs changing on modern systems)
fs.file-max = 2097152

# Per-user limits (/etc/security/limits.conf)
# nero  soft  nofile  65535
# nero  hard  nofile  65535
```

### 7. Connection Tracking

For servers with many concurrent connections (WebSocket, API):

```bash
# Increase conntrack table size
net.netfilter.nf_conntrack_max = 262144
net.netfilter.nf_conntrack_tcp_timeout_established = 86400
```

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Setting vm.swappiness=0 | OOM kills under pressure | Use 10, not 0 |
| Huge TCP buffers on low-RAM server | Memory exhaustion | Scale buffers to RAM |
| Forgetting to apply changes | Settings not active | Run `sudo sysctl --system` |
| Overcommit memory=1 on production | Silent OOM | Keep at 0 (heuristic) |
| Low inotify watches with Claude Code | Watcher errors, missed file changes | Set to 524288 |
| Not testing after changes | Boot failures possible | Test with `sysctl -p file` first |

## Verification Commands

```bash
# Apply all sysctl configs
sudo sysctl --system

# Check a specific value
sysctl net.ipv4.tcp_congestion_control
sysctl fs.inotify.max_user_watches

# Check BBR is active
sysctl net.ipv4.tcp_congestion_control
# Should return: bbr

# Check current inotify usage
find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | cut -d/ -f3 | xargs -I{} sh -c 'cat /proc/{}/cmdline 2>/dev/null | tr "\0" " "; echo ""' | sort | uniq -c | sort -rn | head -10

# Check current file descriptor usage
cat /proc/sys/fs/file-nr
# Format: allocated  free  max

# Check TCP memory usage
cat /proc/net/sockstat

# Check conntrack usage
sudo conntrack -C 2>/dev/null || cat /proc/sys/net/netfilter/nf_conntrack_count
```

## Integration Points

| Component | Integration |
|-----------|------------|
| Docker | Needs high max_map_count, file descriptors |
| RabbitMQ | Needs TCP buffer tuning, file descriptors |
| PostgreSQL | Needs shared memory settings, dirty page tuning |
| Claude Code | Needs high inotify watches |
| nginx | Needs high somaxconn, TCP tuning |
| Swap | vm.swappiness controls swap behavior |
| OOM killer | vm.overcommit and cgroup limits interact |

## References

- [Linux kernel sysctl documentation](https://www.kernel.org/doc/Documentation/sysctl/)
- [Google BBR congestion control](https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster)
- [inotify limits](https://man7.org/linux/man-pages/man7/inotify.7.html)
- [TCP tuning guide](https://fasterdata.es.net/host-tuning/linux/)
- [Ubuntu security hardening](https://wiki.ubuntu.com/Security/Features)
