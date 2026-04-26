#!/bin/bash
# backup.sh
# Full daily backup: PostgreSQL + Redis + configs + restic offsite + retention
#
# Cron: 0 3 * * * /home/nero/workspace/scripts/backup.sh >> /var/log/nero-backup.log 2>&1
# Prerequisites: restic installed, ~/.restic-password exists, B2 credentials in .env

set -euo pipefail

# === Configuration ===
BACKUP_BASE="/home/nero/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/nero-backup.log"
RETENTION_DAYS=14

POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-nero-postgres}"
POSTGRES_USER="${POSTGRES_USER:-nero}"
POSTGRES_DB="${POSTGRES_DB:-nero_db}"

# Load .env for restic and Telegram credentials
if [ -f /home/nero/workspace/.env ]; then
    # shellcheck disable=SC1090
    set -a; source /home/nero/workspace/.env; set +a
fi

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-b2:nero-backups:server}"
export RESTIC_PASSWORD_FILE="/home/nero/.restic-password"

# === Functions ===
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"; }

notify_failure() {
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="BACKUP FAILED on $(hostname): $1" > /dev/null 2>&1 || true
    fi
}

cleanup() {
    [ $? -ne 0 ] && { log "ERROR: Backup failed!"; notify_failure "Check $LOG_FILE for details"; }
}
trap cleanup EXIT

# === Prepare ===
BACKUP_DIR="$BACKUP_BASE/$DATE"
mkdir -p "$BACKUP_DIR/database" "$BACKUP_DIR/redis" "$BACKUP_DIR/configs"

log "=== Backup starting ==="

# === 1. PostgreSQL ===
log "Backing up PostgreSQL..."
docker exec -t "$POSTGRES_CONTAINER" pg_dump \
    -U "$POSTGRES_USER" -Fc "$POSTGRES_DB" > "$BACKUP_DIR/database/${POSTGRES_DB}.dump"

# Verify dump integrity
pg_restore --list "$BACKUP_DIR/database/${POSTGRES_DB}.dump" > /dev/null 2>&1
log "  PostgreSQL: $(du -sh "$BACKUP_DIR/database/${POSTGRES_DB}.dump" | cut -f1) (verified)"

# === 2. Redis ===
log "Backing up Redis..."
docker exec nero-redis redis-cli BGSAVE > /dev/null 2>&1
sleep 2
docker cp nero-redis:/data/dump.rdb "$BACKUP_DIR/redis/dump.rdb"
log "  Redis: $(du -sh "$BACKUP_DIR/redis/dump.rdb" | cut -f1)"

# === 3. Configurations ===
log "Backing up configs..."
cp /home/nero/workspace/.env "$BACKUP_DIR/configs/.env"
sudo cp -r /etc/nginx/sites-available "$BACKUP_DIR/configs/nginx-sites/" 2>/dev/null || true
sudo cp -r /etc/nginx/snippets "$BACKUP_DIR/configs/nginx-snippets/" 2>/dev/null || true
sudo cp -r /etc/nginx/ssl "$BACKUP_DIR/configs/nginx-ssl/" 2>/dev/null || true
cp ~/.config/systemd/user/*.service "$BACKUP_DIR/configs/" 2>/dev/null || true
sudo cp /etc/wireguard/wg0.conf "$BACKUP_DIR/configs/wg0.conf" 2>/dev/null || true
sudo cp /etc/ssh/sshd_config "$BACKUP_DIR/configs/sshd_config" 2>/dev/null || true
crontab -l > "$BACKUP_DIR/configs/crontab.txt" 2>/dev/null || true
sudo cp -r /etc/sysctl.d "$BACKUP_DIR/configs/sysctl.d/" 2>/dev/null || true
log "  Configs backed up"

# === 4. Offsite (restic) ===
log "Uploading to offsite storage..."
restic backup "$BACKUP_DIR" \
    --tag "daily,$(date +%A)" \
    --exclude-caches \
    --quiet 2>> "$LOG_FILE"
log "  Offsite upload complete"

# === 5. Retention ===
log "Applying retention..."
find "$BACKUP_BASE" -maxdepth 1 -type d -name "20*" -mtime +"$RETENTION_DAYS" -exec rm -rf {} \;
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune --quiet 2>> "$LOG_FILE"
log "  Retention applied"

log "=== Backup complete: $(du -sh "$BACKUP_DIR" | cut -f1) ==="
