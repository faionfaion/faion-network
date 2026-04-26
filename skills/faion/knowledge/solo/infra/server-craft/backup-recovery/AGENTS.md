# Backup & Recovery

## Summary

Backup strategy and disaster recovery for solo developer VPS platforms: PostgreSQL with pg_dump, Redis RDB snapshots, configuration file capture, and encrypted offsite backup via restic to Backblaze B2 or S3-compatible storage. Includes retention policy, restore procedures, and a full disaster recovery runbook.

## Why

A solo VPS hosts databases, secrets, and configuration that cannot be reconstructed from Git. The 3-2-1 rule (3 copies, 2 media, 1 offsite) is the minimum viable insurance. Restic provides encryption, deduplication, and retention pruning in a single tool. Without tested backups, an RTO of "hours" becomes "days or never."

## When To Use

- After initial server bootstrap — set up backups before any data lands
- Before destructive operations: database migrations, major upgrades, config refactors
- As part of an automated nightly cron pipeline
- Creating a disaster recovery runbook for a new project
- Auditing existing backup coverage before a production launch

## When NOT To Use

- Ephemeral data that can be fully reconstructed from Git or external APIs
- Application code (already in Git — no separate backup needed)
- Docker images (in registry), Python venvs, node_modules (fully rebuildable)
- Large media files where cloud object storage with versioning is the source of truth

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategy.xml` | 3-2-1 rule, what to back up vs skip, RPO/RTO targets, retention policy |
| `content/02-postgresql.xml` | pg_dump formats, Docker exec pattern, restore commands, verify with pg_restore --list |
| `content/03-restic.xml` | Repository init, backup/forget/prune commands, restore, password management rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/backup.sh` | Full daily backup: pg_dump + Redis + configs + restic upload + retention |
| `templates/verify-backup.sh` | Verify latest backup is valid and recent |
| `templates/restic-wrapper.sh` | Convenience wrapper pre-loading restic env from .env |
