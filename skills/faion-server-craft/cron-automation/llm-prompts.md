# Cron Automation LLM Prompts

## Setup

### Prompt: Design Cron Schedule for VPS

```
Design a complete cron job schedule for my VPS platform.

Server: [OS, specs]
Services: [list all services]
Timezone: [server timezone]

Tasks I need automated:
1. [e.g., Database backup - daily]
2. [e.g., Health monitoring - hourly]
3. [e.g., Log cleanup - weekly]
4. [e.g., Docker cleanup - weekly]
5. [e.g., Certificate check - daily]
6. [e.g., Config sync - every 15 min]
7. [e.g., News digest - daily morning]
8. [e.g., Startup notification - on boot]
9. [Add more as needed]

Requirements:
- Avoid resource conflicts (don't run heavy jobs simultaneously)
- Use flock for long-running jobs
- Log all job output
- Alert on failure via Telegram
- FLOW-style monitoring (hourly/daily/weekly reports)

Provide:
1. Complete crontab with comments
2. Script templates for each job type
3. Schedule visualization (which jobs run when)
4. Log rotation for cron logs
5. Monitoring to ensure cron jobs are running
```

### Prompt: Create Cron Job Script

```
Create a production-ready cron job script for the following task.

Task:
- Description: [what the script should do]
- Schedule: [how often - e.g., daily at 3 AM]
- Dependencies: [what must be running - e.g., PostgreSQL, Redis]
- Env vars needed: [e.g., DATABASE_URL, API_KEY]
- Expected runtime: [e.g., 30 seconds, 5 minutes]
- On failure: [alert via Telegram / ignore / retry]

Server context:
- OS: [e.g., Ubuntu 24.04]
- User: [e.g., nero]
- Env file: [e.g., ~/workspace/.env]
- Log directory: [e.g., /var/log/]

The script must include:
1. Proper shebang and set -euo pipefail
2. Logging to file with timestamps
3. flock locking (prevent overlapping)
4. Error handling with cleanup trap
5. Environment loading
6. The actual task logic
7. Success/failure reporting
```

## Troubleshooting

### Prompt: Debug Cron Job Not Running

```
My cron job is not running. Help me debug.

Crontab entry:
[paste the cron line]

Script path: [path]
Script permissions: [ls -la output]

`crontab -l` output:
[paste]

`systemctl status cron` output:
[paste]

When I run the script manually: [works / fails with error]
Cron log (`grep CRON /var/log/syslog`): [paste relevant lines]

Script content:
[paste script]

Troubleshoot:
1. Is cron daemon running?
2. Is the crontab entry valid? (syntax check)
3. Is the script executable?
4. Is PATH correct for cron environment?
5. Are environment variables available?
6. Is the script's shebang correct?
7. Is output being captured somewhere?
```

### Prompt: Debug Cron Job Failing Silently

```
My cron job appears to run but doesn't produce expected results.

Crontab entry:
[paste]

Script:
[paste script]

Log file contents:
[paste if any log output exists]

Expected result: [what should happen]
Actual result: [what actually happens, or nothing]

When run manually: [works correctly]

The script works manually but fails in cron. Common causes to check:
1. Different PATH in cron
2. Missing environment variables
3. Different working directory
4. Different user context
5. File permissions
6. flock preventing execution
7. STDIN/STDOUT differences

Help me find and fix the issue.
```

### Prompt: Fix Overlapping Cron Jobs

```
I have cron jobs that sometimes overlap, causing issues.

Problematic jobs:
[For each job:]
- Crontab entry: [paste]
- Typical runtime: [e.g., 30 seconds to 5 minutes]
- Problem when overlapping: [what goes wrong]

Help me:
1. Add proper flock locking to each script
2. Set appropriate lock timeout behavior
3. Handle stale lock files (from crashed processes)
4. Add logging when a run is skipped due to lock
5. Monitor for jobs that are chronically locked
```

## FLOW System

### Prompt: Implement FLOW Monitoring

```
I want to implement FLOW-style autonomous monitoring for my server.

FLOW concept:
- Server monitors itself at multiple frequencies
- Higher frequency = simpler check, lower frequency = more detail
- Hourly checks are silent on success (alert only on problems)
- Daily/weekly reports always send

Server:
- Hostname: [name]
- Services to monitor: [list]
- Docker containers: [list]
- Notification: Telegram (bot token and chat ID in .env)

Frequencies I want:
- Hourly: health check (services, Docker, disk, memory, API)
- Every 3 hours: summarize hourly checks
- Daily: full status report (services, resources, errors, backup)
- Weekly: trends (restarts, errors by day, disk growth)
- Monthly: capacity review
- Startup: boot notification

Provide:
1. Complete script for each frequency
2. Crontab entries with proper timing
3. Telegram message formatting (Markdown)
4. Log file management
5. How to test each script
```

## Advanced

### Prompt: Migrate from Cron to systemd Timers

```
I want to migrate some cron jobs to systemd timers for better logging and control.

Current crontab:
[paste relevant entries]

Jobs to migrate:
[list which ones and why]

For each job to migrate, provide:
1. .timer unit file
2. .service unit file
3. Migration steps
4. How to verify the timer works
5. Comparison of cron vs timer behavior for this job
6. Keep remaining jobs in cron

Also explain which jobs should stay in cron and which benefit from timers.
```

### Prompt: Design Cron Monitoring

```
I want to monitor that my cron jobs are actually running as expected.

Current cron jobs:
[list with schedules]

Problems I've had:
- [e.g., "Didn't notice backup job stopped for 3 days"]
- [e.g., "Job was stuck/locked and never ran again"]

Design a monitoring system that:
1. Detects when a job misses its expected run
2. Detects when a job takes much longer than expected
3. Detects stale lock files
4. Sends alerts for any anomaly
5. Provides a daily summary of job health

Provide scripts and crontab entries for the monitoring itself.
```
