# Backup & Recovery

Backup strategy and disaster recovery for solo developer VPS platforms. Covers PostgreSQL, Redis, configuration files, application data, restic for offsite backup, encryption, retention policies, and disaster recovery runbooks.

## Overview

A solo developer VPS hosts everything -- databases, message queues, application code, configuration, secrets. Losing it means losing the entire platform. A proper backup strategy is non-negotiable.

## The 3-2-1 Rule

| Component | Requirement | Solo Dev Implementation |
|-----------|-------------|------------------------|
| **3** | Three copies of data | Production + local backup + offsite |
| **2** | Two different media | Server disk + cloud storage (B2/S3) |
| **1** | One offsite | Backblaze B2 or S3-compatible storage |

For solo developers, 3-2-1 is sufficient. Enterprise patterns (3-2-1-1-0 with immutable storage) add complexity without proportional benefit for personal platforms.

## What to Backup

| Data | Tool | Priority | Frequency | Size Estimate |
|------|------|----------|-----------|---------------|
| PostgreSQL database | pg_dump | Critical | Daily | 50MB-5GB |
| Redis data | redis-cli BGSAVE | Important | Daily | 10-100MB |
| .env / secrets | rsync/restic | Critical | On change | <1KB |
| nginx configs | rsync/restic | Important | On change | <10KB |
| systemd unit files | rsync/restic | Important | On change | <10KB |
| SSL certificates | rsync/restic | Important | On change | <10KB |
| Application attachments | restic | Important | Daily | Variable |
| Crontab | crontab -l | Important | On change | <1KB |
| Git repos | Already on GitHub | Standard | On push | N/A |

**Not backed up** (can be rebuilt):
- Application code (in Git)
- Python .venv directories (rebuilt from requirements.txt)
- Docker images (pulled from registry)
- Docker volumes for RabbitMQ (messages are transient)
- Build artifacts, node_modules

## PostgreSQL Backup

### pg_dump (Logical Backup)

```bash
# Custom format (compressed, supports selective restore)
pg_dump -h localhost -U nero -Fc nero_db > nero_db_$(date +%Y%m%d).dump

# Plain SQL (readable, larger)
pg_dump -h localhost -U nero nero_db > nero_db_$(date +%Y%m%d).sql

# All databases
pg_dumpall -h localhost -U nero > all_databases_$(date +%Y%m%d).sql

# Specific tables
pg_dump -h localhost -U nero -t conversations -t messages nero_db > tables.dump
```

| Format | Flag | Compression | Selective Restore | Use Case |
|--------|------|-------------|-------------------|----------|
| Custom | `-Fc` | Built-in | Yes | Default choice |
| Directory | `-Fd` | Built-in | Yes | Large databases |
| Tar | `-Ft` | No | Yes | Archive compatibility |
| Plain SQL | (default) | No | No | Human-readable |

### Restore

```bash
# Custom format restore
pg_restore -h localhost -U nero -d nero_db --clean --if-exists nero_db.dump

# Plain SQL restore
psql -h localhost -U nero -d nero_db < nero_db.sql

# Restore specific table
pg_restore -h localhost -U nero -d nero_db -t conversations nero_db.dump
```

### Docker PostgreSQL Backup

```bash
# Backup from Docker container
docker compose exec -T postgres pg_dump -U nero -Fc nero_db > nero_db.dump

# Restore to Docker container
docker compose exec -T postgres pg_restore -U nero -d nero_db --clean --if-exists < nero_db.dump
```

## Redis Backup

### RDB Snapshot

```bash
# Trigger a background save
redis-cli BGSAVE

# Check save status
redis-cli LASTSAVE

# Copy the dump file
docker compose exec redis cat /data/dump.rdb > redis_dump_$(date +%Y%m%d).rdb
```

### AOF (Append-Only File)

If AOF is enabled (`appendonly yes`), Redis logs every write operation. The AOF file can be replayed to reconstruct the dataset.

```bash
# Copy AOF file
docker compose exec redis cat /data/appendonly.aof > redis_aof_$(date +%Y%m%d).aof
```

### Restore Redis

```bash
# Stop Redis
docker compose stop redis

# Replace dump.rdb in the volume
docker run --rm -v nero-redis-data:/data -v $(pwd):/backup alpine \
    cp /backup/redis_dump.rdb /data/dump.rdb

# Start Redis (will load dump.rdb)
docker compose start redis
```

## Configuration Backup

### What to Capture

```bash
# All configs worth backing up
/home/nero/workspace/.env                        # Master secrets
/etc/nginx/sites-available/*                      # nginx configs
/etc/nginx/snippets/*                            # nginx SSL snippets
/etc/nginx/ssl/*                                 # SSL certificates
~/.config/systemd/user/*.service                 # systemd services
/etc/wireguard/wg0.conf                          # WireGuard config
/etc/ssh/sshd_config                             # SSH config
/etc/sysctl.d/*.conf                             # Kernel tuning
/etc/fail2ban/jail.d/*                           # Fail2ban jails
~/.tmux.conf                                     # tmux config
~/.bashrc, ~/.bash_aliases                       # Shell config
```

### Config Snapshot Script

```bash
#!/bin/bash
# backup-configs.sh
# Snapshot all server configurations

set -euo pipefail

BACKUP_DIR="/home/nero/backups/configs/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# System configs (need sudo)
sudo cp -r /etc/nginx/sites-available "$BACKUP_DIR/nginx-sites/"
sudo cp -r /etc/nginx/snippets "$BACKUP_DIR/nginx-snippets/"
sudo cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config"
sudo cp -r /etc/sysctl.d "$BACKUP_DIR/sysctl.d/"
sudo cp -r /etc/fail2ban/jail.d "$BACKUP_DIR/fail2ban/"
sudo cp /etc/wireguard/wg0.conf "$BACKUP_DIR/wg0.conf" 2>/dev/null || true

# User configs
cp ~/.config/systemd/user/*.service "$BACKUP_DIR/"
cp ~/workspace/.env "$BACKUP_DIR/.env"
crontab -l > "$BACKUP_DIR/crontab.txt"
cp ~/.tmux.conf "$BACKUP_DIR/tmux.conf" 2>/dev/null || true
cp ~/.bashrc "$BACKUP_DIR/bashrc"
cp ~/.bash_aliases "$BACKUP_DIR/bash_aliases" 2>/dev/null || true

echo "Config backup saved to: $BACKUP_DIR"
ls -la "$BACKUP_DIR"
```

## Restic (Offsite Backup)

Restic is a fast, encrypted, deduplicated backup tool that works with S3, B2, SFTP, and local storage.

### Installation

```bash
sudo apt install restic
```

### Repository Setup (Backblaze B2)

```bash
# Initialize repository
export B2_ACCOUNT_ID="your-b2-account-id"
export B2_ACCOUNT_KEY="your-b2-account-key"
restic init -r b2:bucket-name:nero-backups
```

### Backup Command

```bash
restic backup \
    -r b2:bucket-name:nero-backups \
    /home/nero/backups/database/ \
    /home/nero/backups/configs/ \
    /home/nero/workspace/.env \
    --exclude-caches \
    --tag "daily"
```

### Retention Policy

```bash
restic forget \
    -r b2:bucket-name:nero-backups \
    --keep-daily 7 \
    --keep-weekly 4 \
    --keep-monthly 6 \
    --prune
```

| Policy | Keep | Purpose |
|--------|------|---------|
| --keep-daily 7 | Last 7 days | Quick recovery from recent issues |
| --keep-weekly 4 | Last 4 weeks | Recovery from older issues |
| --keep-monthly 6 | Last 6 months | Long-term archive |

### Verify and Restore

```bash
# List snapshots
restic snapshots -r b2:bucket-name:nero-backups

# Check repository integrity
restic check -r b2:bucket-name:nero-backups

# Restore to a directory
restic restore latest -r b2:bucket-name:nero-backups --target /tmp/restore/

# Restore specific file
restic restore latest -r b2:bucket-name:nero-backups --include "/.env" --target /tmp/
```

## Encryption

Restic encrypts all data by default with AES-256. The repository password is the only thing needed for decryption.

**Store the repository password securely:**
- In your password manager (1Password, Bitwarden)
- In a separate `.restic-password` file (chmod 600, not in backup)
- Never commit to Git

```bash
# Use password file
restic -r b2:bucket-name:nero-backups --password-file ~/.restic-password backup /data
```

## Disaster Recovery Runbook

### Total Server Loss Recovery

1. **Provision new server** (same specs from Hetzner)
2. **Basic setup**: SSH keys, user account, firewall
3. **Install software**: Docker, Python, Node.js, nginx, WireGuard
4. **Restore configs**: nginx, systemd units, SSH, sysctl
5. **Restore secrets**: .env file
6. **Start infrastructure**: Docker Compose (postgres, redis, rabbitmq)
7. **Restore database**: pg_restore from latest backup
8. **Restore Redis**: Copy dump.rdb to volume
9. **Clone code repos**: From GitHub
10. **Deploy applications**: Run deploy.sh, create venvs
11. **Start services**: Enable and start systemd services
12. **Update DNS**: Point domain to new server IP
13. **Verify**: Test all endpoints, check logs
14. **Restore cron**: Import crontab

### RPO/RTO Targets

| Metric | Target | Actual (with daily backups) |
|--------|--------|---------------------------|
| RPO (max data loss) | 24 hours | Up to 24 hours of DB changes |
| RTO (time to recover) | 2 hours | ~1-2 hours with runbook |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| pg_dump fails | Wrong credentials or DB down | Check .env, verify Docker container |
| Restic timeout | Slow network to B2/S3 | Increase timeout, check bandwidth |
| Backup too large | Backing up unnecessary data | Exclude .venv, node_modules, Docker volumes |
| Restore fails | Incompatible PG version | Use same major version for restore |
| Password lost | Restic repo password forgotten | Cannot recover, start new repo |

## Related Methodologies

- `docker-compose-patterns/` -- backing up Docker volumes
- `cron-automation/` -- scheduling backup jobs
- `secrets-management/` -- protecting .env and credentials
- `monitoring-logging/` -- alerting on backup failures
