# Kernel Tuning LLM Prompts

Prompts for AI assistants to audit, tune, and troubleshoot kernel parameters.

## Prompt 1: Kernel Parameter Audit

```
Audit the kernel parameters on this Ubuntu server for a web server + AI agent workload.

Steps:
1. Check OS and kernel version: `uname -r` and `cat /etc/os-release`
2. Check RAM: `free -h`
3. Check CPU: `nproc`
4. List all sysctl.d files: `ls -la /etc/sysctl.d/`
5. Read all sysctl.d configs: `cat /etc/sysctl.d/*.conf`
6. Check key parameters:
   - `sysctl net.ipv4.tcp_congestion_control net.core.default_qdisc`
   - `sysctl fs.inotify.max_user_watches fs.inotify.max_user_instances`
   - `sysctl vm.swappiness vm.dirty_ratio vm.dirty_background_ratio`
   - `sysctl vm.max_map_count fs.file-max`
   - `sysctl kernel.kptr_restrict kernel.yama.ptrace_scope kernel.randomize_va_space`
   - `sysctl net.core.somaxconn net.core.rmem_max net.core.wmem_max`
7. Check file descriptor usage: `cat /proc/sys/fs/file-nr`
8. Check swap usage: `free -h`
9. Check inotify usage: count watches per process

Report as:

| Category | Parameter | Current | Recommended | Status |
|----------|-----------|---------|-------------|--------|
| Network  | ... | ... | ... | OK/TUNE |
| Memory   | ... | ... | ... | OK/TUNE |
| Security | ... | ... | ... | OK/TUNE |
| Agent    | ... | ... | ... | OK/TUNE |

For each TUNE item, provide the exact sysctl.d config file to create.
```

## Prompt 2: Performance Tuning

```
Tune this Ubuntu 24.04 server for optimal performance. The server has {RAM}GB RAM, {CPU} CPUs, and runs:
- Web server (nginx + FastAPI)
- WebSocket connections (long-lived)
- Message queue (RabbitMQ)
- Database (PostgreSQL)
- AI agent workloads (Claude Code, file watchers)
- Docker containers

Create sysctl.d configuration files for:

1. **60-network-perf.conf** — TCP BBR, buffer sizes (scaled to RAM), connection handling, keepalive
2. **60-agent-tuning.conf** — inotify watches, file descriptors, process limits
3. **60-memory.conf** — swappiness, dirty pages, cache pressure, min_free_kbytes

For each file:
- Explain why each parameter is set to that value
- Scale values based on the actual RAM size
- Apply with `sudo sysctl -p /etc/sysctl.d/filename`
- Verify with `sysctl parameter_name`

After applying all files, run `sudo sysctl --system` and verify critical parameters.
```

## Prompt 3: Security Hardening

```
Apply kernel security hardening to this Ubuntu server. This is a production VPS that should not be used for kernel debugging.

Create /etc/sysctl.d/60-security.conf with:

1. Kernel info leakage prevention (kptr_restrict, dmesg_restrict)
2. PTRACE restriction
3. ASLR enforcement
4. SysRq limitation
5. Network security (SYN cookies, ICMP, redirects, source routing, martians)
6. IPv6 security (if IPv6 is used)

For each setting:
- Current value
- Recommended value
- What attack it prevents
- Any compatibility concerns

Apply and verify each setting.
IMPORTANT: Do not disable features needed by Docker or running services.
```

## Prompt 4: Troubleshoot inotify Exhaustion

```
I'm getting "ENOSPC: System limit for number of file watchers reached" errors.

Diagnose and fix:

1. Check current limit: `sysctl fs.inotify.max_user_watches`
2. Check current usage per process:
   ```bash
   find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | \
     cut -d/ -f3 | xargs -I{} sh -c \
     'echo "$(wc -l /proc/{}/fdinfo/$(ls /proc/{}/fd 2>/dev/null | head -1) 2>/dev/null | awk "{print \$1}") $(cat /proc/{}/cmdline 2>/dev/null | tr "\0" " ")"' | \
     sort -rn | head -10
   ```
3. Identify the top consumers
4. Determine the appropriate limit based on usage + headroom
5. Apply the fix:
   ```bash
   echo "fs.inotify.max_user_watches = 524288" | sudo tee /etc/sysctl.d/60-agent-tuning.conf
   sudo sysctl -p /etc/sysctl.d/60-agent-tuning.conf
   ```
6. Verify the fix works
7. Calculate memory impact (1 watch ~ 1 KB)

Also check:
- Are there processes that should not be watching files? (Stop them)
- Can .gitignore / watchman ignore patterns reduce watch count?
```

## Prompt 5: Memory Pressure Troubleshooting

```
The server is experiencing memory pressure / OOM kills / high swap usage.

Diagnose:

1. `free -h` — overall memory and swap usage
2. `cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty|Writeback|Slab"` — detailed breakdown
3. `sysctl vm.swappiness vm.overcommit_memory vm.min_free_kbytes` — current settings
4. `sudo dmesg | grep -i "oom\|killed\|out of memory" | tail -20` — OOM events
5. `ps aux --sort=-%mem | head -15` — top memory consumers
6. `docker stats --no-stream 2>/dev/null` — Docker container memory usage

Based on findings:
- If swapping too aggressively: reduce vm.swappiness
- If OOM kills: identify the memory hog, set cgroup limits
- If dirty pages causing latency: tune vm.dirty_ratio
- If buffer/cache too large: tune vm.vfs_cache_pressure
- If swap is full: add more swap or reduce memory usage

Provide specific sysctl changes and application-level fixes.
```

## Prompt 6: TCP Performance Diagnostics

```
Diagnose TCP performance issues on this server. Users report slow API responses and WebSocket disconnections.

Steps:

1. Check congestion control: `sysctl net.ipv4.tcp_congestion_control`
2. Check buffer sizes: `sysctl net.core.rmem_max net.core.wmem_max net.ipv4.tcp_rmem net.ipv4.tcp_wmem`
3. Check connection stats: `ss -s`
4. Check socket buffer stats: `cat /proc/net/sockstat`
5. Check for connection errors: `netstat -s | grep -E 'segments retransmitted|connection resets|failed connection'`
6. Check listen queue overflow: `netstat -s | grep "SYNs to LISTEN"`
7. Check somaxconn: `sysctl net.core.somaxconn`
8. Check nginx error log for connection issues
9. Check keepalive settings

Based on findings:
- If Cubic: switch to BBR
- If small buffers: increase proportionally to RAM
- If queue overflows: increase somaxconn
- If many retransmissions: check network quality, tune BBR
- If many TIME_WAIT: enable tcp_tw_reuse

Provide the specific sysctl.d file to fix each issue.
```

## Prompt 7: Pre-Deployment Kernel Check

```
I'm deploying a new application on this server. Before deployment, verify the kernel parameters are suitable for:

Application type: {describe the app}
Expected connections: {concurrent connections}
Expected memory usage: {RAM}
File watchers needed: {yes/no}
Docker: {yes/no}

Check and adjust:
1. TCP stack capacity (somaxconn, backlog, buffers)
2. File descriptor limits (system-wide and per-user)
3. inotify watches (if file watchers needed)
4. Memory settings (swappiness, dirty pages, overcommit)
5. Security settings (not compromised by the new app)
6. Docker limits (if Docker is used)

Output a table of current vs required values and the commands to fix any gaps.
```

## Prompt 8: Scaling Kernel Parameters to Hardware

```
This server has:
- RAM: {X} GB
- CPUs: {Y}
- NIC speed: {Z} Gbps
- Workload: {describe workload}

Calculate optimal kernel parameters scaled to this hardware:

1. TCP buffer sizes:
   - max_buffer = NIC_speed_bps * expected_RTT_seconds / 8
   - For 1 Gbps, 100ms RTT: 1e9 * 0.1 / 8 = 12.5 MB -> round to 16 MB

2. somaxconn and backlog:
   - Scale with expected concurrent connections
   - Minimum: 4096, recommended: 65535

3. inotify watches:
   - Memory impact: watches * 1 KB
   - Scale: ensure watches * 1 KB < 2% of RAM

4. vm.min_free_kbytes:
   - Keep 0.5-1% of RAM free for emergencies
   - For {X} GB: {X * 1024 * 0.01} KB

5. dirty page ratios:
   - Scale background_ratio with disk speed (SSD: 5-10%, HDD: 3-5%)

Provide the complete sysctl.d file with all calculated values and explanations.
```
