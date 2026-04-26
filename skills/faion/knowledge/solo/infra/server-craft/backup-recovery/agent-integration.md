# Agent Integration — Backup & Recovery

## When to use
- After initial server bootstrap — first backup job must be set up before any data lands
- Before destructive operations: database migrations, major upgrades, config refactors
- As part of an automated cron pipeline running nightly or on-change
- When a disaster recovery runbook is needed for a new project
- Auditing existing backup coverage before a production launch

## When NOT to use
- Ephemeral data that can be fully reconstructed from Git or external APIs
- Application code (in Git already — no separate backup needed)
- Docker images (in registry), Python venvs, node_modules (fully rebuildable)
- Large media files where cloud object storage with versioning is already the source of truth
- Databases with built-in replication (Postgres streaming replication already provides redundancy)

## Where it fails / limitations
- `pg_dump` fails silently with non-zero exit if DB is down — must check exit code explicitly
- `pg_restore` requires the same major PostgreSQL version as the dump — cross-version restores are not supported
- Restic backup hangs if B2/S3 endpoint is unreachable without an explicit `--timeout` flag
- Restic repository password loss = permanent data loss; there is no recovery path
- Config backups with `sudo cp` fail non-interactively if sudoers requires a TTY — use `NOPASSWD` or `visudo` for backup user
- `redis-cli BGSAVE` is non-blocking; script must poll `LASTSAVE` to confirm the save completed before copying the file
- The 3-2-1 rule is only as good as restore testing — untested backups are not backups

## Agentic workflow
An agent can drive the full backup pipeline: dump the database, snapshot configs, run restic to push offsite, verify the snapshot hash, and send a Telegram confirmation. The critical design principle is that each step must check the previous exit code before proceeding — silent failures in backup pipelines are the most dangerous failure mode. A separate "restore drill" agent should be run monthly against a staging clone to validate recoverability.

### Recommended subagents
- `faion-sdd-executor-agent` — implement backup scripts as SDD tasks with explicit test gates
- `nero-sdd-executor-agent` — NERO platform backup pipeline including all Docker volumes

### Prompt pattern
```
Run the daily backup pipeline for the NERO platform:
1. pg_dump -Fc nero_db > /home/nero/backups/db/nero_$(date +%Y%m%d).dump; check exit code
2. redis-cli BGSAVE; poll LASTSAVE until updated; copy dump.rdb to /home/nero/backups/redis/
3. Run backup-configs.sh (see templates.md)
4. restic backup -r b2:nero-backups /home/nero/backups --password-file ~/.restic-password --tag daily
5. restic forget -r b2:nero-backups --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune --password-file ~/.restic-password
6. If all steps succeed: send Telegram "Backup OK $(date +%Y-%m-%d)"
7. If any step fails: send Telegram "BACKUP FAILED at step N: <error>"
```

```
Perform a restore drill:
1. List latest restic snapshots: restic snapshots -r b2:nero-backups --password-file ~/.restic-password
2. Restore to /tmp/restore-drill/: restic restore latest -r b2:nero-backups --target /tmp/restore-drill/ --password-file ~/.restic-password
3. Verify .env exists in restored files
4. Attempt pg_restore of nero_db dump to a test database nero_db_drill
5. Report: snapshot ID, file count, DB restore exit code
6. Clean up /tmp/restore-drill/ and drop nero_db_drill
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pg_dump` / `pg_restore` | PostgreSQL logical backup/restore | `apt install postgresql-client` |
| `pg_dumpall` | Dump all databases + roles | Same package |
| `redis-cli` | Redis BGSAVE trigger, LASTSAVE check | `apt install redis-tools` |
| `restic` | Encrypted, deduplicated offsite backup | `apt install restic` |
| `rsync` | Config file sync to local directory | `apt install rsync` |
| `rclone` | Cloud storage sync (S3, B2, GCS, etc.) | [rclone.org](https://rclone.org/) |
| `crontab` | Schedule backup jobs | Built-in |
| `logrotate` | Rotate local backup log files | `apt install logrotate` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Backblaze B2 | SaaS | Yes (S3-compatible API) | Cheapest cold storage; restic native support |
| AWS S3 | SaaS | Yes (AWS CLI + restic) | Standard choice; higher cost than B2 |
| Hetzner Storage Box | SaaS | Yes (SFTP/rsync/restic) | Same provider as VPS; fast transfers |
| Cloudflare R2 | SaaS | Yes (S3-compatible) | No egress fees; good for frequent restores |
| BorgBackup | OSS | Yes | Dedup + encryption; similar to restic |
| MinIO | OSS | Yes (S3-compatible) | Self-hosted S3; good for on-prem |
| Litestream | OSS | Yes | Continuous SQLite replication to S3; not Postgres |

## Templates & scripts
See `templates.md` for full backup-configs.sh and the complete daily backup pipeline.

Inline: restic backup wrapper with error handling (≤40 lines):
```bash
#!/bin/bash
# restic-backup.sh — run daily backup with Telegram alert on failure
set -euo pipefail

REPO="b2:nero-backups:nero"
PASS_FILE="$HOME/.restic-password"
LOG="$HOME/backups/logs/restic-$(date +%Y%m%d).log"

mkdir -p "$(dirname "$LOG")"

run_step() {
    local name="$1"; shift
    if "$@" >> "$LOG" 2>&1; then
        echo "OK   $name"
    else
        local rc=$?
        echo "FAIL $name (exit $rc)"
        tg_alert "BACKUP FAILED: $name on $(hostname) — exit $rc"
        exit $rc
    fi
}

tg_alert() {
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d chat_id="$TELEGRAM_CHAT_ID" -d text="$1" > /dev/null
}

run_step "pg_dump"    pg_dump -Fc nero -h localhost -U nero -f "$HOME/backups/db/nero_$(date +%Y%m%d).dump"
run_step "restic-backup"  restic backup -r "$REPO" "$HOME/backups/" --password-file "$PASS_FILE" --tag daily
run_step "restic-forget"  restic forget -r "$REPO" --password-file "$PASS_FILE" \
          --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

tg_alert "Backup OK $(hostname) $(date +%Y-%m-%d)"
```

## Best practices
- Always check `pg_dump` exit code explicitly — it exits 0 even on partial failure with warnings in some versions
- Store restic password in 1Password; also keep an offline copy in a physical safe or printed document
- Run `restic check -r <repo>` monthly to verify repository integrity — bit rot is real in cloud storage
- Separate backup user with NOPASSWD sudo for config files reduces attack surface vs. using the app user
- Test restore quarterly: provision a throwaway VPS, restore everything, verify the platform starts
- Keep retention policy matched to your RPO: 7 daily + 4 weekly + 6 monthly is a sensible solo-dev baseline
- Back up the crontab itself: `crontab -l > ~/backups/configs/crontab.txt` — often forgotten
- Encrypt local backup files too with `age` or `gpg` if the backup directory is on shared storage

## AI-agent gotchas
- `restic` prompts for password interactively if `--password-file` or `$RESTIC_PASSWORD` is not set — agent hangs
- `pg_restore` with `--clean` drops and recreates objects; running it against a live production database is destructive — always restore to a test DB first
- Agent must not assume `redis-cli BGSAVE` is synchronous; must poll `LASTSAVE` in a loop with a timeout
- `sudo cp /etc/nginx/...` in a non-interactive agent session fails if sudoers requires a TTY — add `Defaults !requiretty` for the backup user
- Restic `forget --prune` is slow on large repos and locks the repository — don't run it more than once per day
- B2/S3 credentials must be exported as env vars or in `~/.config/rclone/rclone.conf`; restic doesn't auto-detect 1Password

## References
- [restic documentation](https://restic.readthedocs.io/)
- [Backblaze B2 + restic guide](https://www.backblaze.com/blog/backing-linux-to-backblaze-b2-with-restic/)
- [pg_dump manual](https://www.postgresql.org/docs/current/app-pgdump.html)
- [Redis persistence documentation](https://redis.io/docs/management/persistence/)
- [3-2-1 backup rule — Veeam](https://www.veeam.com/blog/321-backup-rule.html)
