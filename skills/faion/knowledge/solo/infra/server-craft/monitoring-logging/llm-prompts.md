# Monitoring & Logging LLM Prompts

## Setup

### Prompt: Design Monitoring for Solo VPS

```
Design a lightweight monitoring setup for my solo developer VPS.

Server:
- OS: [e.g., Ubuntu 24.04]
- Specs: [e.g., 16 CPUs, 30GB RAM]
- Services: [list systemd services]
- Docker containers: [list]
- Domains: [list]

Requirements:
- No heavy monitoring stacks (no Prometheus/Grafana)
- Alerting via Telegram
- Periodic health reports (FLOW-style: hourly, daily, weekly)
- Log management (rotation, retention)
- At-a-glance dashboard (tmux-based)
- Startup notification on reboot

Provide:
1. journald configuration
2. Health check script (all services, endpoints, resources)
3. Telegram notification setup
4. FLOW monitoring scripts (hourly, daily, startup)
5. tmux dashboard script
6. Cron schedule for all monitoring jobs
7. Log rotation configuration
8. Autoheal service for automatic restarts
```

### Prompt: Setup Alerting

```
I want to set up alerting for my VPS platform via Telegram.

Current setup:
- Services: [list]
- Cron jobs: [list with descriptions]
- Backup job: [schedule]

Alert conditions I want:
- Service goes down
- Docker container stops
- API health check fails
- Disk usage > [threshold]%
- Memory usage > [threshold]%
- Backup fails
- Certificate expiring
- OOM killer triggered
- Server rebooted

Provide:
1. Telegram bot setup instructions
2. Alert script (reusable notify function)
3. Monitoring scripts for each condition
4. Cron schedule for checks
5. Alert format (Markdown for Telegram)
6. Rate limiting (don't spam on flapping)
```

## Log Analysis

### Prompt: Analyze Application Logs

```
Help me analyze logs from my application service.

Service: [name]
Log source: journalctl --user -u [service-name]

Recent log output:
[paste last 50-100 lines of logs]

I'm seeing: [describe the issue - errors, warnings, patterns]

Help me:
1. Identify error patterns and root causes
2. Find timing correlations (when errors occur)
3. Suggest log level adjustments
4. Recommend additional logging for debugging
5. Create a log monitoring query for this specific issue
```

### Prompt: Find Log Patterns

```
I need to create monitoring queries to detect specific issues in my logs.

Issues to detect:
1. [e.g., API timeout errors]
2. [e.g., Database connection failures]
3. [e.g., Memory pressure warnings]
4. [e.g., Authentication failures]

Log sources:
- journalctl --user -u [services]
- Docker logs [containers]
- /var/log/nginx/error.log

For each issue, provide:
1. journalctl/grep command to detect it
2. How to count occurrences per hour
3. Alert threshold recommendation
4. Monitoring script snippet
```

## Troubleshooting

### Prompt: Debug High Resource Usage

```
My server is experiencing high [CPU/memory/disk] usage. Help me investigate.

Current state:
- `top -bn1 | head -20` output: [paste]
- `free -h` output: [paste]
- `df -h` output: [paste]
- `docker stats --no-stream` output: [paste]
- Recent changes: [what changed before the issue started]

Services running: [list with expected resource usage]

Help me:
1. Identify the resource consumer
2. Check for memory leaks (memory growing over time)
3. Check for disk space issues (logs, Docker, temp files)
4. Check for CPU spikes (specific processes)
5. Recommend immediate mitigations
6. Recommend long-term fixes
```

### Prompt: Debug Service Crash Loop

```
A service keeps crashing and restarting. Help me investigate.

Service: [name]
Restart count today: [number]

`systemctl --user status service` output:
[paste]

`journalctl --user -u service --since "1 hour ago"` output:
[paste last 50 lines]

The crash pattern:
- How often: [e.g., every 2-3 minutes]
- Time pattern: [random / specific times / related to events]
- Memory at crash: [if known]
- Exit code: [if known]

Recent changes:
- [code changes, config changes, package updates]

Investigate:
1. Parse crash logs for root cause
2. Check resource limits (MemoryMax, etc.)
3. Check for external dependencies (DB, Redis, API)
4. Determine if it's a memory leak, crash bug, or external cause
5. Recommend fix
```

### Prompt: Investigate OOM Kills

```
One or more processes were OOM-killed. Help me investigate.

`dmesg | grep -i oom` output:
[paste]

`journalctl -k --since "24 hours ago" | grep -i "out of memory"` output:
[paste]

Server specs:
- Total RAM: [e.g., 30GB]
- Swap: [e.g., 4GB]

Current memory usage:
`free -h` output: [paste]
`ps aux --sort=-%mem | head -20` output: [paste]

Services and their MemoryMax settings:
[list services with their memory limits]

Docker container memory limits:
[list containers with deploy.resources.limits.memory]

Help me:
1. Identify which process was killed and why
2. Determine if it's a memory leak or undersized limits
3. Recommend appropriate memory limits for each service
4. Suggest whether swap needs to be increased
5. Configure OOM killer priority if needed
```

## Configuration

### Prompt: Configure Log Rotation

```
I need to set up log rotation for my server.

Log sources:
- journald (systemd services, Docker logs): current size [size]
- /var/log/nero-*.log (application logs): current size [size]
- Docker container logs: current size [size]
- nginx access/error logs: current size [size]

Available disk: [total disk and current usage]
Retention requirements: [how long to keep logs]

Provide:
1. /etc/systemd/journald.conf settings
2. /etc/docker/daemon.json log settings
3. logrotate config for application logs
4. logrotate config for nginx logs
5. Cron job for manual cleanup if needed
6. Commands to verify rotation is working
```

### Prompt: Create FLOW Monitoring System

```
I want to implement FLOW-style autonomous monitoring for my server.

FLOW concept: Server monitors itself at regular intervals and sends periodic reports with varying levels of detail.

Schedules:
- Hourly: Quick health check (alert only on problems)
- Daily: Full status report
- Weekly: Trend analysis, capacity planning
- Monthly: Infrastructure review
- Startup: Boot notification

Server: [describe infrastructure]
Services: [list]
Notification: Telegram

Provide:
1. Hourly health check script (silent when healthy)
2. Daily report script (resource usage, errors, backup status)
3. Weekly report script (trends, growth, capacity warnings)
4. Startup heartbeat script
5. Cron schedule for all scripts
6. Telegram formatting for each report type
```
