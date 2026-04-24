# Swap and Memory Management LLM Prompts

## Memory Troubleshooting

```
Help me diagnose memory issues on my server.

Symptoms:
[DESCRIBE: e.g., "Services are slow", "OOM kills in logs", "Swap usage growing"]

Server details:
- Ubuntu 24.04, 30GB RAM, 4GB swap
- Services: [LIST WITH EXPECTED MEMORY]
- vm.swappiness: [VALUE]

Please:
1. What commands should I run to diagnose?
2. How to identify which process is consuming the most memory
3. How to check if swap is being used and by which processes
4. How to check for memory leaks
5. What to look for in dmesg and journalctl
6. Immediate actions to take
7. Long-term fixes to prevent recurrence

Provide exact commands with expected output format.
```

## OOM Debugging

```
My service was killed by the OOM killer. Help me investigate and prevent this.

What I know:
- Service that was killed: [SERVICE NAME]
- When: [TIMESTAMP or "happened last night"]
- Current memory config:
  - MemoryMax: [VALUE]
  - MemoryHigh: [VALUE]
  - OOMScoreAdjust: [VALUE]

Please:
1. Show me how to find the OOM event in kernel logs
2. Explain what the OOM log output means
3. Identify what triggered the OOM (which process, how much memory)
4. Suggest appropriate MemoryMax/MemoryHigh values
5. Suggest OOMScoreAdjust values for my service hierarchy
6. Should I increase swap or is that masking a problem?
7. How to set up monitoring to catch this earlier

My services (in priority order):
1. PostgreSQL (must survive)
2. Redis (should survive)
3. RabbitMQ (should survive)
4. API gateway (user-facing)
5. Celery workers (can be restarted)
6. Static file server (easy to restart)
```

## Swap Optimization

```
Help me optimize swap configuration for my AI agent platform server.

Server: Ubuntu 24.04, Hetzner CX53
- 16 CPUs, 30GB RAM
- Current swap: [SIZE or "none"]
- Current vm.swappiness: [VALUE or "default (60)"]
- Workload: Python services (FastAPI, Celery), Docker (PostgreSQL, Redis, RabbitMQ)
- Memory usage pattern: [DESCRIBE: e.g., "spikes during LLM API calls"]

Questions:
1. What swap size should I use? (Currently [SIZE])
2. What vm.swappiness value? (Currently [VALUE])
3. Should I use a swap file or swap partition?
4. What other vm.* parameters should I tune?
5. Should I limit swap per service (MemorySwapMax)?
6. How to monitor swap usage over time?

Provide:
- Recommended configuration with rationale
- Exact commands to apply changes
- /etc/sysctl.d/99-memory.conf content
- How to verify changes persist after reboot
```

## Memory Allocation Planning

```
Help me plan memory allocation across multiple services on my server.

Server: [TOTAL RAM, e.g., 30GB]
Swap: [SWAP SIZE, e.g., 4GB]

Services to run:
[LIST WITH EXPECTED MEMORY, e.g.:
- PostgreSQL (shared_buffers=2GB)
- Redis (maxmemory=1.5GB)
- RabbitMQ
- Celery workers (4 processes)
- FastAPI API (2 workers)
- Telegram bot
- React SPA static server
- Auto-heal watcher
]

Questions:
1. How much memory should I allocate to each service?
2. What MemoryMax and MemoryHigh values for each?
3. What OOMScoreAdjust for each?
4. How much headroom should I leave for the OS?
5. Am I overcommitting? Will everything fit?
6. When should I consider upgrading to more RAM?

Output as a table with:
| Service | Expected RSS | MemoryMax | MemoryHigh | OOMScoreAdjust |
```

## Memory Leak Investigation

```
I suspect a memory leak in my [SERVICE_NAME] service.

Evidence:
- Memory grows over time: [describe pattern, e.g., "increases by ~50MB/hour"]
- Process RSS: [current and starting values]
- Service type: [Python/FastAPI/Celery/etc.]

Current setup:
- MemoryMax: [VALUE]
- Restart policy: [on-failure/always]
- Python version: [VERSION]

Please help me:
1. Confirm it's a leak vs expected growth (caching, connection pools)
2. Python tools to profile memory (tracemalloc, objgraph, memory_profiler)
3. How to add memory tracking to my service
4. Quick fix: periodic restart strategy
5. Proper fix: identify and fix the leak

Provide code snippets for memory profiling in [Python/FastAPI/Celery].
```

## cgroups v2 Configuration

```
Help me configure cgroups v2 memory controls via systemd for my services.

I want to set up:
1. Hard memory limits (MemoryMax) for each service
2. Soft limits (MemoryHigh) for throttling before kill
3. Swap limits (MemorySwapMax)
4. Memory reservation (MemoryMin) for critical services
5. OOM handling policy per service

Services:
[LIST WITH PRIORITY AND EXPECTED MEMORY]

Server: Ubuntu 24.04 (cgroups v2 is default)

Provide:
- Complete systemd service file snippets for each service
- Commands to verify cgroup settings are active
- How to monitor cgroup memory usage (systemd-cgtop, manual)
- What happens when MemoryHigh is exceeded vs MemoryMax
- Testing: how to simulate memory pressure
```
