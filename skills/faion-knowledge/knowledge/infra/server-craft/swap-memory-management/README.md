# Swap and Memory Management

## Overview

Memory management for VPS servers running AI agent platforms. Covers swap file creation and tuning, vm.swappiness optimization, OOM killer configuration, PAM limits, systemd memory controls, cgroups v2, and memory monitoring strategies. Designed for servers where multiple Python services (Celery workers, FastAPI, bots) compete for RAM.

**Target:** Ubuntu 24.04 VPS (Hetzner CX53, 16 CPUs, 30GB RAM) running multi-service AI platforms.

## When to Use

| Scenario | Fit |
|----------|-----|
| New server setup (no swap configured) | Essential |
| OOM kills happening on services | Essential |
| Celery workers consuming too much RAM | Essential |
| Setting per-service memory limits | Recommended |
| Optimizing for LLM API response caching | Recommended |
| Planning memory allocation across services | Recommended |
| Debugging memory leaks | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Swap file** | Disk-backed virtual memory, extends RAM when physical memory is full |
| **vm.swappiness** | Kernel parameter (0-200) controlling how aggressively the kernel uses swap |
| **OOM killer** | Kernel mechanism that kills processes when memory is exhausted |
| **oom_score_adj** | Per-process OOM priority (-1000 to 1000), higher = killed first |
| **MemoryMax** | systemd cgroup limit, hard cap on service memory usage |
| **MemoryHigh** | systemd cgroup soft limit, triggers throttling before hard limit |
| **cgroups v2** | Linux kernel resource control, default on Ubuntu 24.04 |
| **PAM limits** | Per-user resource limits via /etc/security/limits.conf |

## Swap File Management

### Sizing Guidelines

| Total RAM | Recommended Swap | Rationale |
|-----------|-----------------|-----------|
| 1-2 GB | 2x RAM (2-4 GB) | Small VPS needs breathing room |
| 4-8 GB | Equal to RAM | Balanced for most workloads |
| 16-32 GB | 2-4 GB | Large RAM, swap is safety net only |
| 32+ GB | 1-2 GB | Minimal swap, mainly for hibernation |

For a 30GB RAM server running AI workloads: **4GB swap** is optimal. Swap is a safety net, not a performance feature.

### Creating a Swap File

```bash
# 1. Create swap file (4GB)
sudo fallocate -l 4G /swapfile

# 2. Set permissions (owner-only read/write)
sudo chmod 600 /swapfile

# 3. Format as swap
sudo mkswap /swapfile

# 4. Enable swap
sudo swapon /swapfile

# 5. Verify
swapon --show
free -h
```

### Making Swap Persistent (/etc/fstab)

```bash
# Add to /etc/fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify fstab is valid (IMPORTANT: broken fstab can prevent boot)
sudo findmnt --verify
```

### Removing/Resizing Swap

```bash
# Disable existing swap
sudo swapoff /swapfile

# Remove from fstab (edit manually)
sudo nano /etc/fstab  # Remove the /swapfile line

# Delete file
sudo rm /swapfile

# Create new size if needed
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## vm.swappiness Tuning

### What swappiness Controls

The `vm.swappiness` parameter (0-200, default 60) controls how aggressively the kernel moves pages from physical RAM to swap. Lower values keep more in RAM; higher values swap more aggressively.

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0 | Only swap to avoid OOM | Database servers, latency-sensitive |
| 10 | Minimal swapping | Recommended for AI/API servers |
| 60 | Default Linux behavior | General-purpose |
| 100 | Aggressive swapping | Memory-constrained systems |

### Setting swappiness

```bash
# Set immediately (non-persistent)
sudo sysctl vm.swappiness=10

# Set persistently
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swap.conf
sudo sysctl --system
```

### Additional vm Parameters

```bash
# /etc/sysctl.d/99-memory.conf

# How aggressively to reclaim memory used for caching
vm.vfs_cache_pressure=50

# Swappiness: keep processes in RAM, only swap under pressure
vm.swappiness=10

# Overcommit: allow moderate overcommit (default=0 is heuristic)
vm.overcommit_memory=0

# Minimum free memory (KB) before triggering reclaim
vm.min_free_kbytes=65536
```

## OOM Killer Configuration

### How OOM Killer Works

When the kernel runs out of memory and swap, it selects a process to kill based on the OOM score. The score combines memory usage with the `oom_score_adj` value.

### oom_score_adj Values

| Value | Meaning | Use For |
|-------|---------|---------|
| -1000 | Never kill (OOM disabled) | Critical system processes only |
| -500 | Very unlikely to be killed | Database, core services |
| 0 | Default | Normal processes |
| 500 | More likely to be killed | Non-critical workers |
| 1000 | Kill first | Sacrificial processes |

### Protecting Critical Services

```ini
# In systemd service file
[Service]
OOMScoreAdjust=-500
```

```bash
# Or set directly for running process
echo -500 | sudo tee /proc/$(pidof celery)/oom_score_adj
```

### Recommended OOM Priority for NERO Platform

| Service | oom_score_adj | Rationale |
|---------|---------------|-----------|
| PostgreSQL | -900 | Data integrity is paramount |
| Redis | -700 | Losing context cache is expensive |
| RabbitMQ | -600 | Message broker must stay up |
| nero-channel-web | -300 | User-facing API gateway |
| nero-channel-tg | -200 | Telegram bridge |
| nero-core (Celery) | 0 | Workers can be restarted |
| nero-web (static) | 100 | Static file server, easy to restart |

## PAM Limits (/etc/security/limits.conf)

### Setting Per-User Limits

```bash
# /etc/security/limits.conf

# Max open files (needed for many connections)
nero    soft    nofile    65536
nero    hard    nofile    65536

# Max processes (prevent fork bombs)
nero    soft    nproc     4096
nero    hard    nproc     4096

# Max virtual memory (KB) - optional safety net
# nero    hard    as        31457280  # 30GB
```

### Verifying Limits

```bash
# Check current limits for running process
cat /proc/$(pidof python3)/limits

# Check limits for current shell
ulimit -a

# Check specific limit
ulimit -n   # open files
ulimit -u   # processes
```

## systemd Memory Controls (cgroups v2)

### Per-Service Memory Limits

```ini
[Service]
# Hard limit: process gets SIGKILL if exceeded
MemoryMax=2G

# Soft limit: kernel throttles but doesn't kill
MemoryHigh=1500M

# Swap limit: max swap usage for this service
MemorySwapMax=512M

# Low memory protection: guaranteed minimum
MemoryMin=256M

# OOM handling
OOMPolicy=stop          # stop service on OOM (default: continue)
OOMScoreAdjust=-300     # Less likely to be killed by system OOM
```

### Recommended Memory Limits for NERO Platform

| Service | MemoryMax | MemoryHigh | Rationale |
|---------|-----------|------------|-----------|
| nero-core (Celery) | 8G | 6G | LLM responses can be large |
| nero-channel-web | 2G | 1500M | FastAPI with connection pool |
| nero-channel-tg | 1G | 768M | Lightweight bot bridge |
| nero-web (serve) | 512M | 384M | Static file server |
| PostgreSQL | 8G | 6G | Shared buffers + work_mem |
| Redis | 4G | 3G | Context cache |
| RabbitMQ | 2G | 1500M | Message queues |

### Monitoring cgroup Usage

```bash
# Check memory usage for a systemd service
systemctl --user status nero-core
# or
systemd-cgtop

# Detailed memory stats
cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/nero-core.service/memory.current
cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/nero-core.service/memory.max
```

## Memory Monitoring

### Essential Commands

```bash
# Overall memory usage
free -h

# Per-process memory (sorted by RSS)
ps aux --sort=-%mem | head -20

# Detailed process memory
pmap -x $(pidof python3) | tail -1

# Swap usage by process
for f in /proc/[0-9]*/status; do
  awk '/VmSwap|Name/{printf $2 " " $3}END{print ""}' "$f"
done | sort -k2 -n -r | head -20

# Watch memory in real-time
watch -n 5 free -h
```

### Alerting on Memory Pressure

```bash
#!/bin/bash
# memory-alert.sh - Alert when memory usage exceeds threshold
THRESHOLD=90
USED_PCT=$(free | awk '/^Mem:/{printf "%.0f", $3/$2 * 100}')

if [ "$USED_PCT" -gt "$THRESHOLD" ]; then
    echo "ALERT: Memory usage at ${USED_PCT}% (threshold: ${THRESHOLD}%)"
    echo "Top memory consumers:"
    ps aux --sort=-%mem | head -6
fi
```

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [server-init-bootstrap](../server-init-bootstrap/) | Swap setup during initial provisioning |
| [health-checks-autoheal](../health-checks-autoheal/) | Memory-aware health checks |
| [multi-project-hosting](../multi-project-hosting/) | Memory allocation across projects |
| [deploy-scripts](../deploy-scripts/) | Memory limit validation during deploy |
