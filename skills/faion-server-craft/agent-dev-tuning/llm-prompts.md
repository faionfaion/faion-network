# Agent Dev Tuning LLM Prompts

## Server Optimization

### Prompt: Tune Server for AI Agent Development

```
I need to optimize my VPS for running AI coding agents (Claude Code).

Server specs:
- OS: [e.g., Ubuntu 24.04]
- CPU: [e.g., 16 cores]
- RAM: [e.g., 30GB]
- Disk: [e.g., 200GB SSD]
- Current swap: [e.g., none / 4GB]

Workload:
- Running services: [list services with memory usage]
- Docker containers: [list with resource usage]
- Number of concurrent agents: [e.g., 1-3]
- Project sizes: [e.g., 5 repos, 10k-50k files total]
- Build tools used: [e.g., pip, npm, webpack]

Current issues:
- [e.g., "Too many open files" errors]
- [e.g., OOM kills during large LLM responses]
- [e.g., File watching slow or failing]

Provide comprehensive tuning for:
1. inotify limits (max_user_watches, instances, events)
2. File descriptor limits (PAM, systemd)
3. Swap configuration and swappiness
4. OOM killer tuning (per-service oom_score_adj)
5. Memory limits for each service (MemoryMax, MemoryHigh)
6. Filesystem tuning (noatime, I/O scheduler)
7. Process priority (nice, ionice)
8. Resource allocation plan (how to split CPU/RAM between services and agents)
9. Verification commands for each change
```

### Prompt: Debug Agent Performance Issues

```
My AI agent (Claude Code) is performing poorly on my server.

Symptoms:
- [e.g., slow file operations, high latency, frequent freezes]
- [e.g., agent killed mid-task]
- [e.g., "inotify watch limit reached"]

Server state during issue:
- `top` output: [paste top 20 lines]
- `free -h` output: [paste]
- `df -h` output: [paste]
- `cat /proc/sys/fs/inotify/max_user_watches`: [value]
- `ulimit -n`: [value]
- `swapon --show`: [paste]
- Recent dmesg/journal: [paste OOM or error messages]

Services running:
[list with PID and memory usage from ps aux]

Diagnose:
1. Is it a memory issue (OOM, swap thrashing)?
2. Is it a file system issue (inotify, open files)?
3. Is it a CPU issue (contention with other services)?
4. Is it a disk I/O issue?
5. Provide specific fixes
```

## Claude Code Configuration

### Prompt: Configure Claude Code for Server Development

```
Help me configure Claude Code (settings.json) for server-side development.

My workflow:
- Work on [N] repositories: [list repos with languages]
- Deploy via: [e.g., rsync + systemd restart]
- Testing: [e.g., pytest, jest]
- Linting: [e.g., ruff, eslint]

Server services I manage:
- [list systemd services]
- [list Docker containers]

I need:
1. Optimal permissions (allow/deny lists)
2. Environment variables for the agent
3. Hooks configuration:
   - Audit logging (what commands agent runs)
   - Notification on agent completion/error
   - Context saving on session end
4. MCP servers for enhanced capability
5. Project-level CLAUDE.md template
6. Custom slash commands for common operations
```

### Prompt: Setup Claude Code Hooks

```
I want to set up Claude Code hooks for my development workflow.

Use cases:
1. [e.g., Log all Bash commands to audit file]
2. [e.g., Send Telegram notification when agent needs input]
3. [e.g., Auto-run tests after code changes]
4. [e.g., Save context when session ends]
5. [e.g., Validate dangerous commands before execution]

Notification channel: [Telegram / none]
Logging: [file path for audit logs]

Provide:
1. Complete hooks configuration for settings.json
2. Supporting scripts that hooks call
3. Installation instructions
4. Testing procedure for each hook
```

## Parallel Agents

### Prompt: Setup Parallel Agent Execution

```
I want to run multiple AI agents simultaneously on my server.

Server specs: [CPU, RAM, disk]
Services already running: [list with resource usage]
Available resources for agents: [estimated CPU and RAM]

Agent workloads:
1. [e.g., Feature development - heavy, many file operations]
2. [e.g., Code review - medium, mostly reading]
3. [e.g., Documentation - light]

Questions:
1. How many agents can I safely run in parallel?
2. How to isolate agents (cgroups, systemd scopes, worktrees)?
3. How to prevent agents from interfering with each other?
4. How to monitor per-agent resource usage?
5. What tmux layout works best for multiple agents?
6. How to use worktrees so agents don't conflict on git?

Provide:
1. Resource allocation plan
2. Agent launch scripts with resource limits
3. Worktree setup commands
4. tmux layout script
5. Monitoring approach
```

### Prompt: Git Worktree Strategy for Agents

```
I want to use git worktrees to let multiple agents work on the same repo.

Repository: [repo name and path]
Branch strategy: [e.g., main + feature branches]
Current agents: [how many, what they do]

Issues to address:
1. How to create worktrees for each agent
2. How to handle shared dependencies (node_modules, .venv)
3. How to merge changes from different agents
4. How to clean up stale worktrees
5. How to avoid conflicts when agents touch the same files

Provide:
1. Worktree naming convention
2. Creation/removal scripts
3. Merge workflow
4. Cleanup automation
5. Best practices for avoiding conflicts
```

## Resource Management

### Prompt: Memory Management for Agent Workloads

```
My agents keep getting OOM-killed. Help me fix memory management.

Server: [RAM, swap, specs]
Current memory layout:
- `free -h` output: [paste]
- `ps aux --sort=-%mem | head -20`: [paste]
- `docker stats --no-stream`: [paste]

Service memory limits:
[list services with their MemoryMax settings]

Agent memory usage pattern:
- Typical: [e.g., 2-4GB]
- Peak (during LLM calls): [e.g., 6-8GB]
- Duration of peaks: [e.g., 10-30 seconds]

OOM kill details:
- `dmesg | grep -i oom`: [paste]
- Which process was killed: [name]
- How often: [frequency]

Help me:
1. Analyze the OOM pattern
2. Right-size service memory limits
3. Configure swap appropriately
4. Set OOM score priorities (protect critical services)
5. Add memory monitoring/alerting
6. Prevent future OOM kills while maximizing agent performance
```

### Prompt: Tune Celery Workers for LLM Tasks

```
I'm running Celery workers that make LLM API calls. Help me tune them.

Current setup:
- Celery pool: [prefork/gevent/solo]
- Concurrency: [number]
- Worker count: [number]
- Current memory usage: [per worker, total]
- Queue configuration: [queue names and routing]

Task characteristics:
- Average task duration: [e.g., 5-30 seconds]
- Task I/O pattern: [e.g., mostly waiting for API response]
- Memory per task: [e.g., 50-200MB during streaming]
- Tasks per minute: [volume]
- Failure rate: [percentage]

Infrastructure:
- Message broker: [RabbitMQ/Redis]
- Result backend: [Redis/PostgreSQL]
- Server specs: [CPU, RAM]

Optimize for:
1. Pool type selection (gevent vs prefork for LLM calls)
2. Concurrency level
3. Memory limits per worker
4. Queue configuration for priority tasks
5. Celery flags (heartbeat, mingle, gossip)
6. Monitoring setup
```
