# Swap and Memory Management Examples

## Example 1: 4GB Swap on 30GB RAM Server

Setting up swap on the NERO Hetzner CX53 server (16 CPUs, 30GB RAM).

### Initial State (No Swap)

```bash
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            30Gi       5.2Gi        22Gi       128Mi       2.8Gi        24Gi
Swap:             0B          0B          0B
```

### Create 4GB Swap

```bash
$ sudo bash swap-create.sh 4G
=== Swap File Setup ===
Size: 4G
File: /swapfile
Creating 4G swap file...
Setting up swapspace version 1, size = 4 GiB
no label, UUID = abcd1234-...
Added to /etc/fstab

=== Swap Status ===
NAME      TYPE SIZE USED PRIO
/swapfile file   4G   0B   -2

               total        used        free      shared  buff/cache   available
Mem:            30Gi       5.2Gi        22Gi       128Mi       2.8Gi        24Gi
Swap:          4.0Gi          0B       4.0Gi

Swap file created and enabled successfully.
```

### Apply Memory Tuning

```bash
$ cat /etc/sysctl.d/99-memory.conf
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.min_free_kbytes=65536

$ sudo sysctl --system | grep -E "swappiness|cache_pressure|min_free"
vm.swappiness = 10
vm.vfs_cache_pressure = 50
vm.min_free_kbytes = 65536
```

### Verify After Reboot

```bash
$ swapon --show
NAME      TYPE SIZE USED PRIO
/swapfile file   4G   0B   -2

$ sysctl vm.swappiness
vm.swappiness = 10
```

## Example 2: OOM Protection for Celery Workers

NERO's Celery workers (nero-core) process LLM API calls and can spike in memory. We protect critical services from OOM while allowing workers to be sacrificed.

### Service Configuration

```ini
# ~/.config/systemd/user/nero-core.service
[Service]
# ... ExecStart and other directives ...

# Memory limits
MemoryMax=8G
MemoryHigh=6G
MemorySwapMax=1G

# OOM: workers can be restarted
OOMScoreAdjust=0
OOMPolicy=stop

# Restart after OOM
Restart=on-failure
RestartSec=5
```

```ini
# Docker: PostgreSQL gets maximum protection
# docker-compose.yml (handled by Docker, not systemd)
# But we can set OOM score via Docker:
services:
  postgres:
    oom_score_adj: -900
```

### Verifying OOM Scores

```bash
# Check OOM score for each service
$ for svc in nero-core nero-channel-web nero-channel-tg nero-web; do
    PID=$(systemctl --user show -p MainPID $svc | cut -d= -f2)
    if [ "$PID" -gt 0 ]; then
        SCORE=$(cat /proc/$PID/oom_score_adj 2>/dev/null || echo "N/A")
        echo "$svc (PID $PID): oom_score_adj=$SCORE"
    else
        echo "$svc: not running"
    fi
done

nero-core (PID 12345): oom_score_adj=0
nero-channel-web (PID 12346): oom_score_adj=-300
nero-channel-tg (PID 12347): oom_score_adj=-200
nero-web (PID 12348): oom_score_adj=100

# Docker containers
$ for container in nero-postgres nero-redis nero-rabbitmq; do
    PID=$(docker inspect --format '{{.State.Pid}}' $container 2>/dev/null)
    if [ -n "$PID" ] && [ "$PID" -gt 0 ]; then
        SCORE=$(cat /proc/$PID/oom_score_adj 2>/dev/null || echo "N/A")
        echo "$container (PID $PID): oom_score_adj=$SCORE"
    fi
done

nero-postgres (PID 1001): oom_score_adj=-900
nero-redis (PID 1002): oom_score_adj=-700
nero-rabbitmq (PID 1003): oom_score_adj=-600
```

### Checking for Past OOM Kills

```bash
# Check kernel log for OOM events
$ dmesg | grep -i "oom\|killed" | tail -5
[83421.123456] Out of memory: Killed process 12345 (celery) total-vm:8192000kB
[83421.123457] oom_reaper: reaped process 12345 (celery), now anon-rss:0kB

# Check journal
$ journalctl -k --since "7 days ago" | grep -i oom
Mar 15 03:42:11 nero-hetzner kernel: nero-core.service: A]
Mar 15 03:42:11 nero-hetzner kernel: Out of memory: Killed process 12345 (celery)
```

## Example 3: Per-Service Memory Limits

Complete systemd memory configuration for all NERO services.

### nero-core.service (Celery Workers)

```ini
[Service]
MemoryMax=8G       # Hard kill above 8GB
MemoryHigh=6G      # Throttle above 6GB
MemorySwapMax=1G   # Allow some swap
OOMScoreAdjust=0   # Default priority
OOMPolicy=stop     # Stop unit on OOM
```

**Rationale:** Celery workers hold LLM responses in memory. A single conversation context can be several MB. With 4 workers processing concurrently, peak usage can reach 4-6GB. The 8GB limit provides headroom for spikes.

### nero-channel-web.service (FastAPI)

```ini
[Service]
MemoryMax=2G
MemoryHigh=1500M
MemorySwapMax=512M
OOMScoreAdjust=-300
OOMPolicy=stop
```

**Rationale:** FastAPI holds connection pools (PostgreSQL, Redis) and active WebSocket connections. Normal usage is 300-500MB, but can spike with many concurrent connections. 2GB limit is generous. Higher OOM protection because it's user-facing.

### nero-channel-tg.service (Telegram Bot)

```ini
[Service]
MemoryMax=1G
MemoryHigh=768M
MemorySwapMax=256M
OOMScoreAdjust=-200
OOMPolicy=stop
```

**Rationale:** Lightweight service, typically uses 100-200MB. The 1GB limit is a safety net.

### nero-web.service (Static Server)

```ini
[Service]
MemoryMax=512M
MemoryHigh=384M
MemorySwapMax=128M
OOMScoreAdjust=100
OOMPolicy=stop
```

**Rationale:** Serves static React SPA files. Minimal memory needs. Lowest OOM protection since it's trivial to restart.

### Monitoring Memory After Configuration

```bash
# Check cgroup memory for each service
$ for svc in nero-core nero-channel-web nero-channel-tg nero-web; do
    CURRENT=$(systemctl --user show $svc -p MemoryCurrent | cut -d= -f2)
    MAX=$(systemctl --user show $svc -p MemoryMax | cut -d= -f2)
    if [ "$CURRENT" != "[not set]" ] && [ "$CURRENT" != "" ]; then
        CURRENT_MB=$((CURRENT / 1048576))
        echo "$svc: ${CURRENT_MB}MB used (max: $MAX)"
    else
        echo "$svc: not running or no cgroup data"
    fi
done

nero-core: 2148MB used (max: 8589934592)
nero-channel-web: 342MB used (max: 2147483648)
nero-channel-tg: 128MB used (max: 1073741824)
nero-web: 52MB used (max: 536870912)
```

## Example 4: Memory Pressure Debugging

A real scenario: the server started swapping heavily after a long conversation with Claude API.

### Symptoms

```bash
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            30Gi        28Gi       256Mi        64Mi       1.8Gi       1.4Gi
Swap:          4.0Gi       2.8Gi       1.2Gi
```

### Investigation

```bash
# Top memory consumers
$ ps aux --sort=-%mem | head -10
USER       PID %CPU %MEM    VSZ   RSS TTY  STAT TIME COMMAND
nero     12345  15.2 25.3 9800000 7740000 ? Sl  2:30 celery -A nero_core worker
nero     12346   3.1  5.2 2100000 1590000 ? Sl  0:45 uvicorn nero_channel_web
postgres  1001   1.2  8.5 3200000 2600000 ? Ss  1:20 postgres
redis     1002   0.5  3.2 1200000  980000 ? Ssl 0:30 redis-server

# Celery worker is using 7.7GB - above MemoryHigh (6G)!
# Check if it's being throttled
$ systemctl --user status nero-core
nero-core.service - NERO Core (Celery Workers)
     Active: active (running) since ...
     Memory: 7.7G (max: 8.0G, high: 6.0G)
     ...
     WARNING: memory usage is above the high mark
```

### Resolution

```bash
# Option 1: Restart the worker (quick fix)
$ systemctl --user restart nero-core

# Option 2: Reduce concurrency
# Edit service file: --concurrency=2 instead of 4
$ systemctl --user edit nero-core
# Add: ExecStart= line with --concurrency=2
$ systemctl --user daemon-reload
$ systemctl --user restart nero-core

# Verify
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            30Gi        8.5Gi       19Gi        64Mi       2.5Gi       21Gi
Swap:          4.0Gi       128Mi       3.9Gi
```

### Post-Mortem: Memory Leak in Response Handling

```python
# The root cause: Celery worker was accumulating context in a global dict
# Fix: Add cleanup after each task

@app.task
def process_message(envelope):
    try:
        result = call_claude_api(envelope)
        return result
    finally:
        # Clean up large response objects
        import gc
        gc.collect()
```
