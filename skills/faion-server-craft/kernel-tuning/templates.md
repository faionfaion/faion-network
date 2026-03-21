# Kernel Tuning Templates

Copy-paste ready sysctl configuration files for Ubuntu 24.04 servers.

## Template 1: Network Performance (`60-network-perf.conf`)

File: `/etc/sysctl.d/60-network-perf.conf`

```bash
# /etc/sysctl.d/60-network-perf.conf
# Network performance tuning for web server + AI agent workload
# Server: 16 CPUs, 30GB RAM, 1Gbps NIC

# --- TCP Congestion Control ---
# BBR provides better throughput and lower latency than Cubic
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr

# --- TCP Buffer Sizes ---
# Scaled for 30GB RAM server with 1Gbps NIC
# Rule of thumb: max buffer = bandwidth * RTT
# 1 Gbps * 100ms RTT = 12.5 MB (set to 16MB for headroom)
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.rmem_default = 1048576
net.core.wmem_default = 1048576

# TCP auto-tuning buffers (min, default, max)
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# --- Connection Handling ---
# Max pending connections in listen() queue
net.core.somaxconn = 65535

# Max packets queued on input (before kernel processes them)
net.core.netdev_max_backlog = 5000

# SYN backlog (pending incomplete connections)
net.ipv4.tcp_max_syn_backlog = 65535

# --- TCP Keepalive ---
# Detect dead connections: start probing after 600s, probe every 60s, 5 probes
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 5

# --- TCP Optimization ---
# Enable TCP Fast Open (client=1 + server=2 = 3)
net.ipv4.tcp_fastopen = 3

# Reuse TIME_WAIT sockets for new connections
net.ipv4.tcp_tw_reuse = 1

# Increase ephemeral port range
net.ipv4.ip_local_port_range = 1024 65535

# Increase max orphaned sockets
net.ipv4.tcp_max_orphans = 65536

# Enable window scaling
net.ipv4.tcp_window_scaling = 1

# Timestamps for PAWS (Protection Against Wrapped Sequences)
net.ipv4.tcp_timestamps = 1

# Enable selective acknowledgments
net.ipv4.tcp_sack = 1
```

## Template 2: Security Hardening (`60-security.conf`)

File: `/etc/sysctl.d/60-security.conf`

```bash
# /etc/sysctl.d/60-security.conf
# Kernel security hardening for production VPS

# --- Kernel Address/Info Leakage ---
# Hide kernel pointers from non-root users
kernel.kptr_restrict = 1

# Restrict dmesg access to root (CAP_SYSLOG)
kernel.dmesg_restrict = 1

# Restrict PTRACE to direct child processes only
kernel.yama.ptrace_scope = 1

# Full Address Space Layout Randomization
kernel.randomize_va_space = 2

# Limited SysRq: sync(16) + remount-ro(32) + reboot(128) = 176
kernel.sysrq = 176

# Protect zero page from userspace mmap
vm.mmap_min_addr = 65536

# --- Network Security ---
# Enable SYN cookies (SYN flood protection)
net.ipv4.tcp_syncookies = 1

# Do not accept ICMP redirects (prevents MITM)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Do not send ICMP redirects (we are not a router)
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Do not accept IP source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Enable source address validation (reverse path filtering)
# 2 = loose mode (compatible with multi-homed servers)
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.default.rp_filter = 2

# Log martian packets (impossible source addresses)
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP broadcast requests (smurf attack prevention)
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore bogus ICMP error responses
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Do not accept router advertisements (we are not using IPv6 SLAAC)
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.default.accept_ra = 0
```

## Template 3: AI Agent Tuning (`60-agent-tuning.conf`)

File: `/etc/sysctl.d/60-agent-tuning.conf`

```bash
# /etc/sysctl.d/60-agent-tuning.conf
# Tuning for AI agent workloads (Claude Code, file watchers, many processes)

# --- inotify ---
# Claude Code + other file watchers consume many inotify watches
# Default 65536 is not enough for large codebases
fs.inotify.max_user_watches = 524288

# Max inotify instances per user
fs.inotify.max_user_instances = 1024

# Max events queued per inotify instance
fs.inotify.max_queued_events = 32768

# --- File Descriptors ---
# System-wide maximum open files
fs.file-max = 2097152

# --- Process Limits ---
# Max PID (allows more concurrent processes)
kernel.pid_max = 131072

# Max threads system-wide
kernel.threads-max = 131072

# --- Memory Maps ---
# Many applications need high vm.max_map_count
# (Elasticsearch, Java, Node.js with many modules)
vm.max_map_count = 1048576

# --- Pipes ---
# Max pipe buffer size (used by subprocess communication)
fs.pipe-max-size = 4194304
```

## Template 4: Memory Management (`60-memory.conf`)

File: `/etc/sysctl.d/60-memory.conf`

```bash
# /etc/sysctl.d/60-memory.conf
# Memory management tuning for 30GB RAM server

# --- Swap Behavior ---
# 10 = prefer RAM, only swap under pressure
# 0 = never swap (dangerous, can cause OOM kills)
# 60 = default (too aggressive for servers with plenty of RAM)
vm.swappiness = 10

# --- Dirty Page Writeback ---
# Start background writeback when 5% of RAM is dirty
vm.dirty_background_ratio = 5

# Force synchronous writeback when 15% of RAM is dirty
vm.dirty_ratio = 15

# Writeback interval (centiseconds = 500ms)
vm.dirty_writeback_centisecs = 500

# Expire dirty pages after 3 seconds
vm.dirty_expire_centisecs = 3000

# --- Cache Behavior ---
# Bias toward keeping inode/dentry caches (vs page cache)
# Lower = keep more inode/dentry cache
vm.vfs_cache_pressure = 50

# --- Memory Overcommit ---
# 0 = heuristic (default, kernel estimates if enough memory)
# 1 = always overcommit (dangerous for production)
# 2 = strict, never overcommit beyond swap+ratio
vm.overcommit_memory = 0

# --- OOM Behavior ---
# Keep 256MB free for emergency (kernel, ssh, etc.)
# 30GB RAM, 256MB = ~0.8%
vm.min_free_kbytes = 262144

# Panic on OOM (let watchdog restart the server)
# 0 = default, kill a process instead of panicking
vm.panic_on_oom = 0

# --- Hugepages ---
# Transparent hugepages: madvise = only use when app requests
# For databases (PostgreSQL), consider setting to 'always'
# Check: cat /sys/kernel/mm/transparent_hugepage/enabled
# Set via kernel boot parameter: transparent_hugepage=madvise
```

## Template 5: Per-User Limits (`99-nero.conf`)

File: `/etc/security/limits.d/99-nero.conf`

```bash
# /etc/security/limits.d/99-nero.conf
# Per-user limits for the nero account

# Open files (needed for many concurrent connections + inotify)
nero  soft  nofile  65535
nero  hard  nofile  65535

# Max processes/threads
nero  soft  nproc   65535
nero  hard  nproc   65535

# Core dump size (0 = disable core dumps for security)
nero  soft  core    0
nero  hard  core    0

# Max locked memory (for mlock, shared memory)
nero  soft  memlock unlimited
nero  hard  memlock unlimited
```

## Template 6: Systemd Service Override for Limits

File: `/etc/systemd/system/nero-core.service.d/limits.conf`

```ini
# Systemd service override for file descriptor limits
# Use when systemd service needs higher limits than PAM defaults

[Service]
LimitNOFILE=65535
LimitNPROC=65535
LimitCORE=0
```

## Template 7: Kernel Tuning Audit Script

```bash
#!/bin/bash
# kernel-audit.sh — Audit current kernel parameters vs recommended

set -euo pipefail

echo "=============================="
echo "  Kernel Parameters Audit"
echo "  $(hostname) — $(date)"
echo "=============================="

# Define recommended values
declare -A RECOMMENDED=(
    ["net.ipv4.tcp_congestion_control"]="bbr"
    ["net.core.default_qdisc"]="fq"
    ["fs.inotify.max_user_watches"]="524288"
    ["fs.inotify.max_user_instances"]="1024"
    ["vm.swappiness"]="10"
    ["vm.dirty_ratio"]="15"
    ["vm.dirty_background_ratio"]="5"
    ["vm.max_map_count"]="1048576"
    ["kernel.kptr_restrict"]="1"
    ["kernel.dmesg_restrict"]="1"
    ["kernel.yama.ptrace_scope"]="1"
    ["kernel.randomize_va_space"]="2"
    ["net.ipv4.tcp_syncookies"]="1"
    ["net.ipv4.conf.all.accept_redirects"]="0"
    ["net.ipv4.conf.all.send_redirects"]="0"
    ["net.core.somaxconn"]="65535"
    ["fs.file-max"]="2097152"
)

printf "%-45s %-15s %-15s %s\n" "Parameter" "Current" "Recommended" "Status"
printf "%-45s %-15s %-15s %s\n" "---------" "-------" "-----------" "------"

for param in $(echo "${!RECOMMENDED[@]}" | tr ' ' '\n' | sort); do
    current=$(sysctl -n "$param" 2>/dev/null || echo "N/A")
    recommended="${RECOMMENDED[$param]}"

    if [ "$current" = "$recommended" ]; then
        status="OK"
    else
        status="TUNE"
    fi

    printf "%-45s %-15s %-15s %s\n" "$param" "$current" "$recommended" "$status"
done

echo ""
echo "--- Memory ---"
free -h | head -2
echo ""
echo "--- File Descriptors ---"
cat /proc/sys/fs/file-nr
echo "(allocated  free  max)"
echo ""
echo "--- TCP Connections ---"
ss -s | head -5
```
