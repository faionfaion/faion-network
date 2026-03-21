# Backup & Recovery Templates

## Comprehensive Backup Script

```bash
#!/bin/bash
# backup.sh
# Full backup: PostgreSQL + Redis + configs -> local + offsite (restic)
# Run daily via cron: 0 3 * * * /home/nero/workspace/scripts/backup.sh

set -euo pipefail

# === Configuration ===
BACKUP_BASE="/home/nero/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/nero-backup.log"
RETENTION_DAYS=14

# Database settings (from .env or hardcoded)
POSTGRES_CONTAINER="nero-postgres"
POSTGRES_USER="${POSTGRES_USER:-nero}"
POSTGRES_DB="${POSTGRES_DB:-nero_db}"

# Restic settings
export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-b2:nero-backups:server}"
export RESTIC_PASSWORD_FILE="/home/nero/.restic-password"
export B2_ACCOUNT_ID="${B2_ACCOUNT_ID}"
export B2_ACCOUNT_KEY="${B2_ACCOUNT_KEY}"

# Notification (Telegram)
NOTIFY_ON_FAILURE=true
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# === Functions ===
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"
}

notify_failure() {
    if [ "$NOTIFY_ON_FAILURE" = true ] && [ -n "$BOT_TOKEN" ]; then
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -d chat_id="$CHAT_ID" \
            -d text="BACKUP FAILED on $(hostname): $1" > /dev/null 2>&1 || true
    fi
}

cleanup() {
    if [ $? -ne 0 ]; then
        log "ERROR: Backup failed!"
        notify_failure "Check $LOG_FILE for details"
    fi
}
trap cleanup EXIT

# === Prepare ===
BACKUP_DIR="$BACKUP_BASE/$DATE"
mkdir -p "$BACKUP_DIR/database" "$BACKUP_DIR/redis" "$BACKUP_DIR/configs"

log "=== Backup starting ==="

# === 1. PostgreSQL Backup ===
log "Backing up PostgreSQL..."
docker exec -t "$POSTGRES_CONTAINER" pg_dump \
    -U "$POSTGRES_USER" \
    -Fc "$POSTGRES_DB" > "$BACKUP_DIR/database/${POSTGRES_DB}.dump"

DUMP_SIZE=$(du -sh "$BACKUP_DIR/database/${POSTGRES_DB}.dump" | cut -f1)
log "  PostgreSQL dump: $DUMP_SIZE"

# Verify dump
pg_restore --list "$BACKUP_DIR/database/${POSTGRES_DB}.dump" > /dev/null 2>&1
log "  PostgreSQL dump verified"

# === 2. Redis Backup ===
log "Backing up Redis..."
docker exec nero-redis redis-cli BGSAVE > /dev/null 2>&1
sleep 2  # Wait for BGSAVE to complete
docker cp nero-redis:/data/dump.rdb "$BACKUP_DIR/redis/dump.rdb"

REDIS_SIZE=$(du -sh "$BACKUP_DIR/redis/dump.rdb" | cut -f1)
log "  Redis dump: $REDIS_SIZE"

# === 3. Configuration Backup ===
log "Backing up configs..."

# .env (critical)
cp /home/nero/workspace/.env "$BACKUP_DIR/configs/.env"

# nginx
sudo cp -r /etc/nginx/sites-available "$BACKUP_DIR/configs/nginx-sites/" 2>/dev/null || true
sudo cp -r /etc/nginx/snippets "$BACKUP_DIR/configs/nginx-snippets/" 2>/dev/null || true
sudo cp -r /etc/nginx/ssl "$BACKUP_DIR/configs/nginx-ssl/" 2>/dev/null || true

# systemd
cp ~/.config/systemd/user/*.service "$BACKUP_DIR/configs/" 2>/dev/null || true

# WireGuard
sudo cp /etc/wireguard/wg0.conf "$BACKUP_DIR/configs/wg0.conf" 2>/dev/null || true

# SSH
sudo cp /etc/ssh/sshd_config "$BACKUP_DIR/configs/sshd_config"

# Crontab
crontab -l > "$BACKUP_DIR/configs/crontab.txt" 2>/dev/null || true

# sysctl
sudo cp -r /etc/sysctl.d "$BACKUP_DIR/configs/sysctl.d/" 2>/dev/null || true

log "  Configs backed up"

# === 4. Offsite Backup (restic) ===
log "Uploading to offsite storage..."

restic backup \
    "$BACKUP_DIR" \
    --tag "daily,$(date +%A)" \
    --exclude-caches \
    --quiet 2>> "$LOG_FILE"

log "  Offsite upload complete"

# === 5. Retention ===
log "Applying retention policy..."

# Local: keep 14 days
find "$BACKUP_BASE" -maxdepth 1 -type d -name "20*" -mtime +"$RETENTION_DAYS" -exec rm -rf {} \;

# Offsite: keep 7 daily, 4 weekly, 6 monthly
restic forget \
    --keep-daily 7 \
    --keep-weekly 4 \
    --keep-monthly 6 \
    --prune \
    --quiet 2>> "$LOG_FILE"

log "  Retention applied"

# === Summary ===
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "=== Backup complete: $TOTAL_SIZE ==="
```

## Restic Wrapper Script

```bash
#!/bin/bash
# restic-wrapper.sh
# Convenience wrapper for restic commands with pre-configured environment
# Usage: ./restic-wrapper.sh snapshots
#        ./restic-wrapper.sh restore latest --target /tmp/restore

set -euo pipefail

# Load restic environment
export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-b2:nero-backups:server}"
export RESTIC_PASSWORD_FILE="/home/nero/.restic-password"

# Load B2 credentials from .env
if [ -f /home/nero/workspace/.env ]; then
    eval "$(grep -E '^(B2_ACCOUNT_ID|B2_ACCOUNT_KEY)=' /home/nero/workspace/.env)"
    export B2_ACCOUNT_ID B2_ACCOUNT_KEY
fi

# Pass all arguments to restic
exec restic "$@"
```

## Cron Schedule Template

```cron
# Backup schedule for NERO platform
# Edit with: crontab -e

# Daily full backup at 3 AM
0 3 * * * /home/nero/workspace/scripts/backup.sh >> /var/log/nero-backup.log 2>&1

# Weekly restic repository check (Sunday 5 AM)
0 5 * * 0 /home/nero/workspace/scripts/restic-wrapper.sh check >> /var/log/nero-backup.log 2>&1
```

## Restore Runbook

```markdown
# NERO Platform Disaster Recovery Runbook

## Prerequisites

- [ ] New server provisioned (Ubuntu 24.04, Hetzner CX53)
- [ ] SSH access configured
- [ ] Restic repository password available
- [ ] B2/S3 credentials available

## Phase 1: Server Setup (15 min)

1. Update system:
   apt update && apt upgrade -y

2. Create nero user:
   adduser nero
   usermod -aG sudo nero
   loginctl enable-linger nero

3. Install packages:
   apt install -y docker.io docker-compose-v2 nginx certbot \
     python3-pip python3-venv nodejs npm git restic wireguard

4. Add nero to docker group:
   usermod -aG docker nero

## Phase 2: Restore Configs (10 min)

1. Download latest backup:
   su - nero
   export RESTIC_REPOSITORY="b2:nero-backups:server"
   export RESTIC_PASSWORD_FILE=~/.restic-password
   # (create password file first)
   restic restore latest --target /tmp/restore

2. Restore .env:
   mkdir -p ~/workspace
   cp /tmp/restore/*/configs/.env ~/workspace/.env
   chmod 600 ~/workspace/.env

3. Restore nginx:
   sudo cp -r /tmp/restore/*/configs/nginx-sites/* /etc/nginx/sites-available/
   sudo cp -r /tmp/restore/*/configs/nginx-snippets/* /etc/nginx/snippets/
   sudo mkdir -p /etc/nginx/ssl
   sudo cp -r /tmp/restore/*/configs/nginx-ssl/* /etc/nginx/ssl/

4. Restore systemd services:
   mkdir -p ~/.config/systemd/user
   cp /tmp/restore/*/configs/*.service ~/.config/systemd/user/
   systemctl --user daemon-reload

5. Restore crontab:
   crontab /tmp/restore/*/configs/crontab.txt

6. Restore SSH config:
   sudo cp /tmp/restore/*/configs/sshd_config /etc/ssh/sshd_config
   sudo systemctl restart sshd

## Phase 3: Infrastructure (10 min)

1. Clone nero-infra:
   mkdir -p ~/workspace/repos
   cd ~/workspace/repos
   git clone https://github.com/faionfaion/nero-infra.git

2. Start Docker services:
   cd nero-infra
   cp ~/workspace/.env .env
   docker compose up -d

3. Wait for health checks:
   docker compose ps  # All should be "healthy"

## Phase 4: Restore Data (10 min)

1. Restore PostgreSQL:
   docker compose exec -T postgres pg_restore \
     -U nero -d nero_db --clean --if-exists \
     < /tmp/restore/*/database/nero_db.dump

2. Restore Redis:
   docker compose stop redis
   docker cp /tmp/restore/*/redis/dump.rdb nero-redis:/data/dump.rdb
   docker compose start redis

## Phase 5: Deploy Applications (15 min)

1. Clone all repos:
   cd ~/workspace/repos
   for repo in nero-sdk nero-core nero-channel-web nero-channel-tg nero-web; do
     git clone https://github.com/faionfaion/$repo.git
   done

2. Deploy all:
   bash ~/workspace/deploy/deploy.sh all --rebuild-venv

3. Start services:
   systemctl --user enable --now nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal

## Phase 6: DNS & Verification (5 min)

1. Update DNS:
   - Cloudflare: point A record to new server IP
   - Or update nginx upstream

2. Verify:
   curl http://127.0.0.1:8100/health
   systemctl --user status 'nero-*'
   docker compose ps

## Total estimated recovery time: ~60 minutes
```

## Backup Verification Script

```bash
#!/bin/bash
# verify-backup.sh
# Verify the latest backup is valid and complete

set -euo pipefail

BACKUP_BASE="/home/nero/backups"
LATEST=$(ls -td "$BACKUP_BASE"/20* 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
    echo "FAIL: No backups found"
    exit 1
fi

echo "=== Verifying backup: $LATEST ==="
ERRORS=0

# Check PostgreSQL dump
DUMP="$LATEST/database/nero_db.dump"
if [ -f "$DUMP" ]; then
    if pg_restore --list "$DUMP" > /dev/null 2>&1; then
        echo "OK   PostgreSQL dump: $(du -sh "$DUMP" | cut -f1)"
    else
        echo "FAIL PostgreSQL dump is corrupted"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "FAIL PostgreSQL dump missing"
    ERRORS=$((ERRORS + 1))
fi

# Check Redis dump
RDB="$LATEST/redis/dump.rdb"
if [ -f "$RDB" ] && [ -s "$RDB" ]; then
    echo "OK   Redis dump: $(du -sh "$RDB" | cut -f1)"
else
    echo "FAIL Redis dump missing or empty"
    ERRORS=$((ERRORS + 1))
fi

# Check critical configs
for cfg in .env sshd_config; do
    if [ -f "$LATEST/configs/$cfg" ]; then
        echo "OK   Config: $cfg"
    else
        echo "FAIL Config missing: $cfg"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check age
AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$LATEST")) / 3600 ))
if [ "$AGE_HOURS" -gt 25 ]; then
    echo "WARN Backup is $AGE_HOURS hours old (expected < 25)"
    ERRORS=$((ERRORS + 1))
else
    echo "OK   Backup age: ${AGE_HOURS}h"
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "RESULT: $ERRORS issues found"
    exit 1
else
    echo "RESULT: All checks passed"
fi
```
