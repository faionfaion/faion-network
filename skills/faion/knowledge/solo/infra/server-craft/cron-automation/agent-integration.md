# Agent Integration — Cron Automation

## When to use
- Scheduling recurring server-side tasks: backups, log cleanup, health checks, report delivery
- Implementing FLOW-style multi-frequency autonomous monitoring (hourly/daily/weekly cadence)
- Running deploy post-hooks on a timer rather than manually triggering them
- Draining queues or syncing config files at a fixed cadence
- `@reboot` tasks that must start when the server boots (e.g., start a worker if systemd unit is not set up)

## When NOT to use
- Tasks that need reliable journald logging and missed-run recovery → use systemd timers instead
- Application-level scheduling tied to the Django/Celery stack → use Celery Beat
- Tasks that need resource limits (CPU cap, memory max) → systemd timer with `MemoryMax=`
- Dependency ordering between tasks → systemd `After=`/`Wants=` is necessary
- High-frequency sub-minute scheduling → cron minimum resolution is 1 minute; use a loop service

## Where it fails / limitations
- Cron runs with minimal PATH (`/usr/bin:/bin`); scripts that call project binaries fail silently unless PATH is set explicitly in crontab header or script
- No built-in missed-run recovery — if server is down during a scheduled run, the job is skipped
- `MAILTO=""` must be set or cron emails all output to local mail, which piles up unread
- flock prevents overlaps but a stale lock file (from killed process) causes the next run to be skipped until manually cleared
- Cron has no concept of dependencies — parallel jobs can race on shared resources (same DB, same log file)
- The systemd journal backend must be used for services that log via journal; `logpath`-based tools miss those entries

## Agentic workflow
An agent writing a new cron job reads the existing crontab (`crontab -l`), checks for schedule conflicts and duplicate entries, generates the script file following the standard template (lock, log, cleanup trap, source env), installs the script to the canonical path, appends the crontab entry, and verifies by listing the crontab again. For FLOW-style monitoring, the agent generates all frequency scripts from a shared template with per-frequency alert thresholds injected.

### Recommended subagents
- `bash-agent` — generates cron scripts from template, installs them, edits crontab, verifies
- `monitoring-agent` — reads log files from scheduled jobs and reports anomalies to Telegram

### Prompt pattern
```
Generate a cron script for the following task: <task description>.
Requirements:
- Use the standard template: set -euo pipefail, LOG_FILE, flock, trap cleanup EXIT, source .env
- Schedule: <cron expression>
- Script path: /home/nero/workspace/scripts/<name>.sh
- Log path: /var/log/nero-<name>.log
Return the full script and the crontab line to add.
```

```
Read the crontab for user nero (`crontab -l`). Check for:
1. Duplicate schedule entries for the same script
2. Missing MAILTO="" at the top
3. Scripts that reference absolute paths that do not exist
Report issues and propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `crontab` | Edit, list, and install cron jobs | built-in / `man 5 crontab` |
| `flock` | File-based locking to prevent overlapping runs | built-in (`util-linux`) |
| `systemctl list-timers` | Compare with systemd timers | built-in |
| `journalctl -u cron` | Debug cron daemon issues | built-in |
| `crontab.guru` | Validate cron expressions interactively | [crontab.guru](https://crontab.guru/) |
| `anacron` | Run missed jobs on next boot | `apt install anacron` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| systemd timers | OSS (built-in) | Yes — `systemctl` | Better logging and dependency; preferred for critical tasks |
| Healthchecks.io | SaaS | Yes — HTTP ping | Monitors that a cron job ran; alerts if missed |
| Cronitor | SaaS | Yes — HTTP ping | SaaS cron monitoring with dashboard |
| Telegram Bot API | SaaS | Yes — `curl` POST | FLOW monitoring sends alerts via Telegram |

## Templates & scripts
See `templates.md` for the full standard cron script template.

Minimal compliant cron script (inline, 30 lines):
```bash
#!/bin/bash
# backup-postgres.sh
# Cron: 0 3 * * * /home/nero/workspace/scripts/backup-postgres.sh

set -euo pipefail

LOG_FILE="/var/log/nero-backup-postgres.log"
LOCK_FILE="/tmp/backup-postgres.lock"
BACKUP_DIR="/srv/backups/postgres"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"; }

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "ERROR: Already running, skipping"
    exit 1
fi

cleanup() {
    local rc=$?
    [ $rc -ne 0 ] && log "ERROR: Failed with exit code $rc"
}
trap cleanup EXIT

source /home/nero/workspace/.env 2>/dev/null || true

log "Starting backup"
mkdir -p "$BACKUP_DIR"
pg_dumpall -U postgres | gzip > "$BACKUP_DIR/all-$(date +%Y%m%d).sql.gz"
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete
log "Done"
```

## Best practices
- Set `SHELL=/bin/bash` and full `PATH` at the top of every crontab — never assume defaults
- Set `MAILTO=""` to suppress email output; redirect stdout/stderr to log files explicitly (`>> /var/log/name.log 2>&1`)
- Always use `flock` for any job that could run longer than its schedule interval
- Log both start and end timestamps — a job that starts but never logs "Done" is hung
- Use Healthchecks.io or Cronitor for critical jobs (backups, deploys) — adds missed-run alerting with zero code
- For FLOW monitoring, the hourly script must be silent on success; only alert on anomalies to avoid alert fatigue
- Stagger jobs by 5-10 minutes from each other to avoid simultaneous resource spikes at the top of the hour
- Store crontab as a file in the project repo (`crontab.txt`) and manage with `crontab crontab.txt` for version control

## AI-agent gotchas
- **Human-in-loop checkpoint:** Before adding a `@reboot` cron entry or modifying the backup job schedule, confirm with the operator — these have side effects on server startup and data retention
- **Cron environment is not the user's shell environment.** Agents that test a script manually (it works) then add it to cron (it fails) forget that `~/.bashrc` and user PATH are not loaded. Always use absolute paths for all binaries in scripts
- **flock stale lock detection:** If an agent kills a running cron script mid-execution, the lock file remains and the next scheduled run silently skips. Agents must check for stale locks (`lsof /tmp/script.lock`) before diagnosing "job not running" issues
- **Log rotation:** Cron log files grow indefinitely unless logrotate is configured. Agents generating new cron jobs must also add a logrotate rule or use `>` (truncate) instead of `>>` for low-value logs
- **Testing cron expressions:** Agents must not trust their own cron expression generation without validation against `crontab.guru` or running `crontab -l` and confirming the next-run time

## References
- [cron and crontab manual](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [flock manual](https://man7.org/linux/man-pages/man1/flock.1.html)
- [systemd timers vs cron](https://wiki.archlinux.org/title/Systemd/Timers)
- [Healthchecks.io](https://healthchecks.io/)
- [crontab.guru](https://crontab.guru/)
