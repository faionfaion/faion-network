# Kernel Tuning Examples

Real-world kernel tuning configurations and benchmarks for Hetzner CX53 running NERO AI platform.

## Example 1: NERO Production Server (Current State)

**Server:** Ubuntu 24.04, Hetzner CX53, 16 CPUs, 30GB RAM, NVMe SSD

### Current sysctl.d Files

```
/etc/sysctl.d/
  10-console-messages.conf     # kernel.printk = 4 4 1 7
  10-ipv6-privacy.conf        # net.ipv6.conf.*.use_tempaddr = 2
  10-kernel-hardening.conf     # kernel.kptr_restrict = 1
  10-magic-sysrq.conf         # kernel.sysrq = 176
  10-map-count.conf           # vm.max_map_count = 1048576
  10-network-security.conf    # net.ipv4.conf.*.rp_filter = 2
  10-ptrace.conf              # kernel.yama.ptrace_scope = 1
  10-zeropage.conf            # vm.mmap_min_addr = 65536
  99-sysctl.conf              # -> /etc/sysctl.conf (mostly comments)
```

### Current vs Recommended

| Parameter | Current | Recommended | Action |
|-----------|---------|-------------|--------|
| tcp_congestion_control | cubic | bbr | Add 60-network-perf.conf |
| default_qdisc | fq_codel | fq | Add 60-network-perf.conf |
| max_user_watches | 65536 | 524288 | Add 60-agent-tuning.conf |
| swappiness | 60 | 10 | Add 60-memory.conf |
| dirty_ratio | 20 | 15 | Add 60-memory.conf |
| somaxconn | 4096 | 65535 | Add 60-network-perf.conf |
| kptr_restrict | 1 | 1 | Already set |
| ptrace_scope | 1 | 1 | Already set |
| max_map_count | 1048576 | 1048576 | Already set |

### Commands to Apply

```bash
# Create custom config files
sudo tee /etc/sysctl.d/60-network-perf.conf << 'EOF'
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
EOF

sudo tee /etc/sysctl.d/60-agent-tuning.conf << 'EOF'
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.inotify.max_queued_events = 32768
fs.file-max = 2097152
kernel.pid_max = 131072
vm.max_map_count = 1048576
EOF

sudo tee /etc/sysctl.d/60-memory.conf << 'EOF'
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.vfs_cache_pressure = 50
vm.min_free_kbytes = 262144
EOF

# Apply
sudo sysctl --system

# Verify
sysctl net.ipv4.tcp_congestion_control fs.inotify.max_user_watches vm.swappiness
```

## Example 2: Before/After BBR Benchmarks

### Test Setup

```bash
# Install iperf3 on both client and server
sudo apt install -y iperf3

# Server side
iperf3 -s

# Client side (from a remote machine)
iperf3 -c server-ip -t 30 -P 4
```

### Before (Cubic + fq_codel)

```
$ sysctl net.ipv4.tcp_congestion_control
net.ipv4.tcp_congestion_control = cubic

$ iperf3 -c 168.119.x.x -t 30 -P 4
[  5]   0.00-30.00  sec   238 MBytes  66.5 Mbits/sec    0
[  7]   0.00-30.00  sec   241 MBytes  67.4 Mbits/sec    0
[  9]   0.00-30.00  sec   237 MBytes  66.3 Mbits/sec    0
[ 11]   0.00-30.00  sec   240 MBytes  67.1 Mbits/sec    0
[SUM]   0.00-30.00  sec   956 MBytes   267 Mbits/sec    0
```

### After (BBR + fq)

```
$ sysctl net.ipv4.tcp_congestion_control
net.ipv4.tcp_congestion_control = bbr

$ iperf3 -c 168.119.x.x -t 30 -P 4
[  5]   0.00-30.00  sec   283 MBytes  79.2 Mbits/sec    0
[  7]   0.00-30.00  sec   279 MBytes  78.0 Mbits/sec    0
[  9]   0.00-30.00  sec   281 MBytes  78.6 Mbits/sec    0
[ 11]   0.00-30.00  sec   280 MBytes  78.3 Mbits/sec    0
[SUM]   0.00-30.00  sec  1123 MBytes   314 Mbits/sec    0
```

**Result:** ~18% throughput improvement with BBR on a Hetzner CX53 with 1Gbps NIC. The improvement is more dramatic on lossy or high-latency connections (50-100% improvement possible).

## Example 3: inotify Watch Exhaustion

### Problem: Claude Code fails with "ENOSPC: System limit for inotify watches reached"

```bash
# Check current usage
$ find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | cut -d/ -f3 | \
    xargs -I{} sh -c 'wc -l /proc/{}/fdinfo/* 2>/dev/null | tail -1' | \
    awk '{sum += $1} END {print sum}'
52341

# Current limit
$ sysctl fs.inotify.max_user_watches
fs.inotify.max_user_watches = 65536

# Claude Code alone is using 52k watches!
```

### Fix

```bash
# Increase to 524288 (8x default)
echo "fs.inotify.max_user_watches = 524288" | sudo tee /etc/sysctl.d/60-agent-tuning.conf
sudo sysctl -p /etc/sysctl.d/60-agent-tuning.conf

# Verify
sysctl fs.inotify.max_user_watches
# fs.inotify.max_user_watches = 524288
```

### Memory Impact

Each inotify watch consumes approximately 1 KB of kernel memory:

| Watches | Memory Usage |
|---------|-------------|
| 65,536 (default) | ~64 MB |
| 524,288 (recommended) | ~512 MB |
| 1,048,576 (maximum) | ~1 GB |

On a 30GB RAM server, 512 MB for inotify watches is acceptable.

## Example 4: Swappiness Tuning for AI Workloads

### Problem: Server swaps too aggressively, causing latency spikes

```bash
# Default swappiness = 60
$ sysctl vm.swappiness
vm.swappiness = 60

# Check swap usage
$ free -h
              total        used        free      shared  buff/cache   available
Mem:           29Gi       8.2Gi       2.1Gi       312Mi        19Gi        20Gi
Swap:         4.0Gi       1.8Gi       2.2Gi

# 1.8GB swapped out despite 20GB available!
# This happens because swappiness=60 is too aggressive for servers with lots of RAM.
```

### Fix

```bash
# Set swappiness to 10
sudo sysctl -w vm.swappiness=10

# Move swapped data back to RAM (if needed)
sudo swapoff -a && sudo swapon -a

# Verify
$ free -h
              total        used        free      shared  buff/cache   available
Mem:           29Gi        10Gi       512Mi       312Mi        19Gi        18Gi
Swap:         4.0Gi          0B       4.0Gi
```

### Swappiness Values Guide

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0 | Never swap (dangerous) | Avoid |
| 10 | Swap only under heavy pressure | Production server with ample RAM |
| 30 | Light swapping | General server |
| 60 | Default, moderate swapping | General purpose |
| 100 | Aggressive swapping | Memory-constrained systems |

## Example 5: Connection Handling for WebSocket-Heavy Workloads

### Problem: nginx "connection reset by peer" errors under load

```bash
# Check somaxconn (listen queue limit)
$ sysctl net.core.somaxconn
net.core.somaxconn = 4096

# nginx error log shows:
# *1234 connect() to 127.0.0.1:8100 failed (111: Connection refused)

# Check SYN backlog
$ sysctl net.ipv4.tcp_max_syn_backlog
net.ipv4.tcp_max_syn_backlog = 4096
```

### Fix: Increase connection handling capacity

```bash
# Increase connection queue sizes
sudo sysctl -w net.core.somaxconn=65535
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sudo sysctl -w net.core.netdev_max_backlog=5000

# Also update nginx to match
# In /etc/nginx/nginx.conf:
# worker_connections 8192;
# In server block:
# listen 443 ssl backlog=4096;
```

### WebSocket Connection Profile

For NERO's WebSocket connections (long-lived, low bandwidth per connection):

```bash
# Optimize TCP keepalive for WebSocket
net.ipv4.tcp_keepalive_time = 600      # Start probing after 10 min idle
net.ipv4.tcp_keepalive_intvl = 60      # Probe every 60 seconds
net.ipv4.tcp_keepalive_probes = 5      # Give up after 5 failed probes
# Total timeout: 600 + (60 * 5) = 900 seconds (15 minutes)

# This matches the nginx proxy_read_timeout = 86400 setting
# nginx handles the WS keepalive, kernel handles TCP keepalive
```

## Example 6: File Descriptor Limits for RabbitMQ

### Problem: RabbitMQ hitting file descriptor limit

```bash
# RabbitMQ log shows:
# file descriptor limit: 1024
# Recommended: 65536

# Check system-wide limit
$ sysctl fs.file-max
fs.file-max = 9223372036854775807  # Default on modern kernels (unlimited)

# Check per-process limit for RabbitMQ container
$ docker exec nero-rabbitmq cat /proc/1/limits | grep "open files"
Max open files            1024                 1048576              files
```

### Fix: Set Docker container limits

```yaml
# docker-compose.yml
services:
  rabbitmq:
    image: rabbitmq:3-management
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
    # ... rest of config
```

Also set host-level limits:
```bash
# /etc/security/limits.d/99-nero.conf
nero  soft  nofile  65535
nero  hard  nofile  65535
```

## Example 7: Monitoring Kernel Parameters

### Automated Check Script (for cron)

```bash
#!/bin/bash
# /usr/local/bin/kernel-check.sh
# Run daily via cron: 0 6 * * * /usr/local/bin/kernel-check.sh

ALERT=""

# Check BBR
CC=$(sysctl -n net.ipv4.tcp_congestion_control)
[ "$CC" != "bbr" ] && ALERT="$ALERT\nWARN: TCP CC is $CC (expected bbr)"

# Check inotify
IW=$(sysctl -n fs.inotify.max_user_watches)
[ "$IW" -lt 524288 ] && ALERT="$ALERT\nWARN: inotify watches = $IW (expected >= 524288)"

# Check swappiness
SW=$(sysctl -n vm.swappiness)
[ "$SW" -gt 20 ] && ALERT="$ALERT\nWARN: swappiness = $SW (expected <= 20)"

# Check swap usage
SWAP_USED=$(free | awk '/Swap:/{print $3}')
SWAP_TOTAL=$(free | awk '/Swap:/{print $2}')
if [ "$SWAP_TOTAL" -gt 0 ]; then
    SWAP_PCT=$((SWAP_USED * 100 / SWAP_TOTAL))
    [ "$SWAP_PCT" -gt 50 ] && ALERT="$ALERT\nWARN: Swap usage = ${SWAP_PCT}%"
fi

# Check file descriptor usage
FD_INFO=$(cat /proc/sys/fs/file-nr)
FD_USED=$(echo "$FD_INFO" | awk '{print $1}')
FD_MAX=$(echo "$FD_INFO" | awk '{print $3}')
FD_PCT=$((FD_USED * 100 / FD_MAX))
[ "$FD_PCT" -gt 80 ] && ALERT="$ALERT\nWARN: File descriptors = ${FD_PCT}% used"

if [ -n "$ALERT" ]; then
    echo -e "Kernel parameter alerts on $(hostname):\n$ALERT"
    # Could send to Slack, email, etc.
fi
```
