# Cron Automation Checklist

## Pre-Setup

- [ ] Verify cron daemon is running: `systemctl status cron`
- [ ] Check current crontab: `crontab -l`
- [ ] Identify timezone: `timedatectl` (cron uses system timezone)
- [ ] Plan job schedule (avoid conflicts and resource spikes)
- [ ] Create scripts directory: `~/workspace/scripts/`
- [ ] Create log directory (or use /var/log/)

## Script Quality

### Every Script Must Have

- [ ] Shebang line: `#!/bin/bash`
- [ ] Error handling: `set -euo pipefail`
- [ ] Logging function that writes to log file
- [ ] Lock file with flock (prevent overlapping runs)
- [ ] Error trap with cleanup function
- [ ] Environment loading (source .env)
- [ ] Executable permission: `chmod +x script.sh`

### Script Testing

- [ ] Run script manually and verify it works
- [ ] Run with minimal PATH to simulate cron: `env -i PATH=/usr/bin:/bin HOME=$HOME bash script.sh`
- [ ] Verify log output is captured
- [ ] Verify lock file prevents duplicate runs
- [ ] Verify error handling works (introduce intentional error)

## Crontab Setup

### Header

- [ ] Set SHELL=/bin/bash
- [ ] Set full PATH
- [ ] Set MAILTO="" (disable mail, use log files instead)
- [ ] Add comments for each job section

### Job Entries

- [ ] Each job has a descriptive comment
- [ ] Each job redirects output: `>> /var/log/name.log 2>&1`
- [ ] Jobs use absolute paths for scripts
- [ ] Schedule avoids midnight pileup (spread across hours)
- [ ] Resource-heavy jobs run at off-peak times

### Schedule Review

- [ ] No two heavy jobs run at the same time
- [ ] Backup jobs don't conflict with application peak usage
- [ ] Health checks run at :00, other jobs offset by minutes
- [ ] Weekly/monthly jobs don't all run on the same day
- [ ] @reboot jobs have appropriate sleep delay

## Monitoring Jobs

### FLOW System (if implemented)

- [ ] Hourly health check configured
- [ ] Daily report configured
- [ ] Weekly report configured
- [ ] Startup heartbeat configured
- [ ] All FLOW scripts tested individually
- [ ] Telegram notifications working

### Backup Jobs

- [ ] Daily database backup cron entry
- [ ] Weekly integrity check cron entry
- [ ] Backup job has failure alerting
- [ ] Backup job has flock locking

### Cleanup Jobs

- [ ] Docker system prune (weekly)
- [ ] Old log file cleanup
- [ ] Temp file cleanup
- [ ] Old backup file retention

## Verification

### Cron Operation

- [ ] All cron jobs listed: `crontab -l`
- [ ] No duplicate entries
- [ ] All scripts are executable
- [ ] All log files are being written to
- [ ] Lock files work (no overlapping runs)

### Job Results

- [ ] Check each job's log file for recent successful runs
- [ ] Verify daily backup ran: check backup directory
- [ ] Verify health checks ran: check FLOW log
- [ ] Verify cleanup jobs ran: check disk usage trends

### Failure Handling

- [ ] Test failure scenario for critical jobs
- [ ] Verify failure alerts are sent (Telegram)
- [ ] Verify flock prevents zombie locks after crash
- [ ] Verify logs capture error messages

## Documentation

- [ ] All cron jobs documented in server runbook
- [ ] Backup crontab to a file: `crontab -l > ~/workspace/configs/crontab.txt`
- [ ] Include crontab in configuration backup
- [ ] Document schedule rationale (why this time/frequency)

## Maintenance

- [ ] Monthly: review cron job logs for issues
- [ ] Monthly: verify all jobs are still running
- [ ] Quarterly: review if any jobs are unnecessary
- [ ] On change: update crontab backup file
- [ ] On change: verify new job doesn't conflict with existing
