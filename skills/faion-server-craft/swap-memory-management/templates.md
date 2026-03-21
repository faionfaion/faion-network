# Swap and Memory Management Templates

## swap-create.sh

Complete script to create, enable, and persist a swap file.

```bash
#!/bin/bash
# swap-create.sh - Create and enable swap file
# Usage: sudo bash swap-create.sh [size]
# Example: sudo bash swap-create.sh 4G
set -euo pipefail

SWAP_SIZE="${1:-4G}"
SWAP_FILE="/swapfile"

echo "=== Swap File Setup ==="
echo "Size: $SWAP_SIZE"
echo "File: $SWAP_FILE"

# Check if swap already exists
if swapon --show | grep -q "$SWAP_FILE"; then
    echo "Swap file $SWAP_FILE already active"
    echo "To resize: sudo swapoff $SWAP_FILE && sudo rm $SWAP_FILE && sudo bash $0 $SWAP_SIZE"
    exit 0
fi

# Check if file exists but not active
if [ -f "$SWAP_FILE" ]; then
    echo "Swap file exists but is not active. Removing and recreating."
    rm -f "$SWAP_FILE"
fi

# Create swap file
echo "Creating ${SWAP_SIZE} swap file..."
fallocate -l "$SWAP_SIZE" "$SWAP_FILE"

# Set permissions (security: only root should read swap)
chmod 600 "$SWAP_FILE"

# Format as swap
mkswap "$SWAP_FILE"

# Enable swap
swapon "$SWAP_FILE"

# Add to fstab if not already there
if ! grep -q "$SWAP_FILE" /etc/fstab; then
    echo "$SWAP_FILE none swap sw 0 0" >> /etc/fstab
    echo "Added to /etc/fstab"
fi

# Verify
echo ""
echo "=== Swap Status ==="
swapon --show
echo ""
free -h | head -3
echo ""
echo "Swap file created and enabled successfully."
```

## sysctl Memory Configuration

```bash
# /etc/sysctl.d/99-memory.conf
# Memory and swap optimization for AI agent platform
# Apply with: sudo sysctl --system

# Swappiness: 10 = minimal swapping, keep processes in RAM
# Range: 0-200, default: 60
# For AI/API servers: 10 (use swap only under memory pressure)
vm.swappiness=10

# VFS cache pressure: how aggressively to reclaim dentry/inode caches
# Range: 0-1000, default: 100
# 50 = keep more filesystem metadata in cache
vm.vfs_cache_pressure=50

# Minimum free memory (KB) before kernel triggers memory reclaim
# Default: varies by RAM, usually ~67MB
# 65536 = 64MB reserved for emergency allocations
vm.min_free_kbytes=65536

# Overcommit: 0=heuristic (default), 1=always allow, 2=strict
# 0 is fine for most servers
vm.overcommit_memory=0

# Dirty page writeback: when to start writing dirty pages to disk
# 10% of RAM = trigger background writeback
vm.dirty_ratio=10

# 5% of RAM = trigger foreground writeback
vm.dirty_background_ratio=5

# Max map count (needed for Elasticsearch, some Python apps)
# Default: 65530, increase if services need many memory mappings
vm.max_map_count=262144
```

## systemd Service with Memory Limits

Template for a systemd user service with full memory controls.

```ini
# ~/.config/systemd/user/nero-core.service
[Unit]
Description=NERO Core (Celery Workers)
After=network.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-core/src
EnvironmentFile=/srv/nero/.env

ExecStart=/srv/nero/nero-core/.venv/bin/celery \
    -A nero_core worker \
    --loglevel=info \
    --concurrency=4

# ============================================================
# Memory Controls (cgroups v2)
# ============================================================

# Hard limit: SIGKILL if exceeded (no recovery)
MemoryMax=8G

# Soft limit: kernel throttles process, tries to reclaim
MemoryHigh=6G

# Maximum swap usage for this service
MemorySwapMax=1G

# Minimum guaranteed memory (protects from other services)
# MemoryMin=512M

# ============================================================
# OOM Configuration
# ============================================================

# OOM score adjustment (-1000 to 1000)
# Lower = less likely to be killed
# Workers: 0 (default, can be sacrificed)
OOMScoreAdjust=0

# What to do when OOM kills this service
# stop = stop the service unit
# continue = keep running (default)
# kill = just let the process die
OOMPolicy=stop

# ============================================================
# Restart Policy
# ============================================================
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5

[Install]
WantedBy=default.target
```

## Memory Limit Templates Per Service Type

### API Server (FastAPI/uvicorn)

```ini
[Service]
MemoryMax=2G
MemoryHigh=1500M
MemorySwapMax=512M
OOMScoreAdjust=-300
OOMPolicy=stop
```

### Celery Worker

```ini
[Service]
MemoryMax=8G
MemoryHigh=6G
MemorySwapMax=1G
OOMScoreAdjust=0
OOMPolicy=stop
```

### Telegram Bot

```ini
[Service]
MemoryMax=1G
MemoryHigh=768M
MemorySwapMax=256M
OOMScoreAdjust=-200
OOMPolicy=stop
```

### Static File Server

```ini
[Service]
MemoryMax=512M
MemoryHigh=384M
MemorySwapMax=128M
OOMScoreAdjust=100
OOMPolicy=stop
```

## memory-alert.sh

Memory monitoring and alerting script.

```bash
#!/bin/bash
# memory-alert.sh - Alert when memory usage exceeds threshold
# Usage: bash memory-alert.sh [threshold_percent]
# Can be run via cron: */5 * * * * bash /path/to/memory-alert.sh 85

set -euo pipefail

THRESHOLD="${1:-90}"
ALERT_SCRIPT="${HOME}/workspace/scripts/alert.sh"

# Calculate memory usage percentage
USED_PCT=$(free | awk '/^Mem:/{printf "%.0f", $3/$2 * 100}')
SWAP_PCT=$(free | awk '/^Swap:/{if($2>0) printf "%.0f", $3/$2 * 100; else print "0"}')

HOSTNAME=$(hostname)
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Check RAM
if [ "$USED_PCT" -gt "$THRESHOLD" ]; then
    MSG="MEMORY ALERT on ${HOSTNAME}
RAM usage: ${USED_PCT}% (threshold: ${THRESHOLD}%)
Swap usage: ${SWAP_PCT}%

Top memory consumers:
$(ps aux --sort=-%mem | head -6 | awk '{printf "%-6s %-5s %s\n", $4"%", $11, $1}')"

    echo "$MSG"

    # Send alert if script exists
    if [ -x "$ALERT_SCRIPT" ]; then
        bash "$ALERT_SCRIPT" "$MSG"
    fi
fi

# Check swap (if swap is more than 50% used, something is wrong)
if [ "$SWAP_PCT" -gt 50 ]; then
    MSG="SWAP ALERT on ${HOSTNAME}
Swap usage: ${SWAP_PCT}%
RAM usage: ${USED_PCT}%

This indicates memory pressure. Consider:
1. Increasing RAM or swap
2. Reducing service memory limits
3. Investigating memory leaks"

    echo "$MSG"

    if [ -x "$ALERT_SCRIPT" ]; then
        bash "$ALERT_SCRIPT" "$MSG"
    fi
fi
```

## PAM Limits Template

```bash
# /etc/security/limits.conf
# Format: <domain> <type> <item> <value>

# Service user: increased file and process limits
nero    soft    nofile    65536
nero    hard    nofile    65536
nero    soft    nproc     4096
nero    hard    nproc     4096

# Optional: memory limits (in KB)
# nero    hard    as        31457280     # 30GB virtual memory
# nero    hard    rss       15728640     # 15GB resident memory

# Root: higher limits
root    soft    nofile    65536
root    hard    nofile    65536
```

## Memory Baseline Documentation Template

```markdown
# Memory Baseline: [Server Name]

| Date | Total RAM | Used | Free | Swap Used | Notes |
|------|-----------|------|------|-----------|-------|
| YYYY-MM-DD | 30G | 18G | 12G | 0G | Normal operation |

## Per-Service Memory Usage

| Service | RSS (avg) | RSS (peak) | MemoryMax | Notes |
|---------|-----------|------------|-----------|-------|
| nero-core | 2.1G | 4.5G | 8G | Spikes during LLM calls |
| nero-channel-web | 350M | 600M | 2G | Connection pools |
| nero-channel-tg | 120M | 200M | 1G | Lightweight |
| nero-web | 50M | 80M | 512M | Static serving |
| postgres | 1.8G | 3G | - | shared_buffers=2G |
| redis | 500M | 1G | - | maxmemory=1.5G |
| rabbitmq | 200M | 400M | - | Default limits |

## Total Budget

| Category | Allocated | Actual |
|----------|-----------|--------|
| OS + kernel | 1G | ~0.8G |
| Backing services | 7G | ~2.5G |
| NERO services | 12G | ~2.6G |
| Other projects | 6G | ~0G |
| Swap buffer | 4G | 0G |
| **Total** | **30G** | **~5.9G** |
```
