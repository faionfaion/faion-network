# Backup & Recovery Examples

## Example 1: NERO Platform Daily Backup

The NERO platform runs a daily backup at 3 AM that captures PostgreSQL, Redis, and all configuration files, then uploads to Backblaze B2 via restic.

### Backup Flow

```
3:00 AM cron triggers backup.sh
  |
  +-> pg_dump nero_db -> /home/nero/backups/YYYYMMDD/database/
  +-> redis BGSAVE -> /home/nero/backups/YYYYMMDD/redis/
  +-> cp configs -> /home/nero/backups/YYYYMMDD/configs/
  |     .env, nginx, systemd, ssh, crontab, wireguard
  |
  +-> restic backup -> b2:nero-backups (encrypted, deduplicated)
  +-> restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6
  +-> local cleanup (delete > 14 days)
  +-> log results to /var/log/nero-backup.log
```

### Crontab

```cron
# Daily full backup at 3 AM
0 3 * * * /home/nero/workspace/scripts/backup.sh >> /var/log/nero-backup.log 2>&1

# Weekly integrity check (Sunday 5 AM)
0 5 * * 0 /home/nero/workspace/scripts/restic-wrapper.sh check >> /var/log/nero-backup.log 2>&1
```

### Storage Costs

| Provider | Plan | Monthly Cost | Storage |
|----------|------|-------------|---------|
| Backblaze B2 | Pay-per-use | ~$0.50 | ~100GB with dedup |

### Monitoring

The FLOW system's daily report includes backup status:

```bash
# In flow-send-daily.sh:
echo "## Backup Status"
LAST_BACKUP=$(ls -td /home/nero/backups/20* 2>/dev/null | head -1)
if [ -n "$LAST_BACKUP" ]; then
    AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$LAST_BACKUP")) / 3600 ))
    SIZE=$(du -sh "$LAST_BACKUP" | cut -f1)
    echo "Last backup: $(basename "$LAST_BACKUP") ($SIZE, ${AGE_HOURS}h ago)"
else
    echo "WARNING: No backups found!"
fi
```

---

## Example 2: Emergency Database Restore

Scenario: A bad migration corrupted the `conversations` table. Need to restore just that table from yesterday's backup.

### Step 1: Find the Backup

```bash
# List local backups
ls -la /home/nero/backups/
# drwxr-xr-x 5 nero nero 4096 Mar 21 03:15 20260321_030000
# drwxr-xr-x 5 nero nero 4096 Mar 20 03:12 20260320_030000

# Or from restic
restic snapshots
# ID        Time                 Host    Tags      Paths
# a1b2c3d4  2026-03-21 03:15:00  nero    daily     /home/nero/backups/20260321_030000
# e5f6g7h8  2026-03-20 03:12:00  nero    daily     /home/nero/backups/20260320_030000
```

### Step 2: List Tables in Dump

```bash
pg_restore --list /home/nero/backups/20260320_030000/database/nero_db.dump | grep "TABLE DATA"
# 3001; 0 16384 TABLE DATA public conversations nero
# 3002; 0 16385 TABLE DATA public messages nero
# 3003; 0 16386 TABLE DATA public users nero
```

### Step 3: Restore Single Table

```bash
# Method 1: Restore just the conversations table
docker compose exec -T postgres pg_restore \
    -U nero -d nero_db \
    --data-only \
    -t conversations \
    /home/nero/backups/20260320_030000/database/nero_db.dump

# Method 2: Restore to a temporary database first (safer)
docker compose exec postgres createdb -U nero nero_db_restore
docker compose exec -T postgres pg_restore \
    -U nero -d nero_db_restore \
    /home/nero/backups/20260320_030000/database/nero_db.dump

# Verify data in temp database
docker compose exec postgres psql -U nero -d nero_db_restore \
    -c "SELECT count(*) FROM conversations;"

# Copy specific table data from temp to production
docker compose exec postgres psql -U nero -d nero_db -c "
    TRUNCATE conversations;
    INSERT INTO conversations
    SELECT * FROM dblink(
        'dbname=nero_db_restore user=nero',
        'SELECT * FROM conversations'
    ) AS t(/* column definitions */);
"

# Or simpler: dump from temp, restore to prod
docker compose exec -T postgres pg_dump -U nero -t conversations --data-only nero_db_restore | \
    docker compose exec -T postgres psql -U nero -d nero_db

# Clean up temp database
docker compose exec postgres dropdb -U nero nero_db_restore
```

### Step 4: Verify

```bash
docker compose exec postgres psql -U nero -d nero_db -c "
    SELECT count(*) as total,
           min(created_at) as earliest,
           max(created_at) as latest
    FROM conversations;
"
```

---

## Example 3: Full Server Recovery Drill

A quarterly exercise to verify the disaster recovery runbook works.

### Environment

```
Production server: Hetzner CX53, 203.0.113.50
Test server: Hetzner CX22, 198.51.100.100 (temporary, ~$4/mo)
```

### Step 1: Provision Test Server

```bash
# Via Hetzner Cloud API or console
# Ubuntu 24.04, CX22, same region

# SSH to test server
ssh root@198.51.100.100

# Create nero user
adduser nero
usermod -aG sudo nero
su - nero
```

### Step 2: Install Dependencies

```bash
sudo apt update && sudo apt install -y \
    docker.io docker-compose-v2 nginx \
    python3-pip python3-venv nodejs npm \
    git restic

sudo usermod -aG docker nero
loginctl enable-linger nero
```

### Step 3: Restore from Restic

```bash
# Set up restic credentials
echo "your-restic-password" > ~/.restic-password
chmod 600 ~/.restic-password

export RESTIC_REPOSITORY="b2:nero-backups:server"
export RESTIC_PASSWORD_FILE=~/.restic-password
export B2_ACCOUNT_ID="your-id"
export B2_ACCOUNT_KEY="your-key"

# List available snapshots
restic snapshots

# Restore latest
restic restore latest --target /tmp/restore

# Restore configs
mkdir -p ~/workspace
cp /tmp/restore/*/configs/.env ~/workspace/.env
mkdir -p ~/.config/systemd/user
cp /tmp/restore/*/configs/*.service ~/.config/systemd/user/
```

### Step 4: Start Infrastructure

```bash
mkdir -p ~/workspace/repos
cd ~/workspace/repos
git clone https://github.com/faionfaion/nero-infra.git
cd nero-infra
ln -s ~/workspace/.env .env
docker compose up -d

# Wait for healthy
sleep 30
docker compose ps
```

### Step 5: Restore Data

```bash
# PostgreSQL
docker compose exec -T postgres pg_restore \
    -U nero -d nero_db --clean --if-exists \
    < /tmp/restore/*/database/nero_db.dump

# Verify
docker compose exec postgres psql -U nero -d nero_db \
    -c "SELECT count(*) FROM conversations;"
```

### Step 6: Deploy Apps

```bash
cd ~/workspace/repos
for repo in nero-sdk nero-core nero-channel-web nero-channel-tg nero-web; do
    git clone https://github.com/faionfaion/$repo.git
done

# Create deploy directory
mkdir -p ~/workspace/deploy
# Copy deploy script from git or restore

# Deploy all
bash ~/workspace/deploy/deploy.sh all --rebuild-venv
```

### Step 7: Verify

```bash
curl http://127.0.0.1:8100/health
systemctl --user status 'nero-*'
```

### Step 8: Document Results

```markdown
## DR Drill Results - 2026-03-21

### Timing
- Server provisioned: 5 min
- Dependencies installed: 8 min
- Restic restore: 12 min (850MB downloaded)
- Infrastructure started: 3 min
- Database restored: 4 min
- Apps deployed: 15 min
- Verification: 3 min
- **Total RTO: 50 minutes**

### Issues Found
1. deploy.sh references absolute paths specific to prod server
2. Missing restic-wrapper.sh from backup
3. Node.js version mismatch (prod has 20, fresh install got 18)

### Action Items
- [ ] Update deploy.sh to use relative paths
- [ ] Include scripts/ directory in backup
- [ ] Document required Node.js version in runbook
```

### Step 9: Tear Down

```bash
# Delete test server via Hetzner console
# Cost: ~$0.01 for 1 hour of CX22
```

---

## Example 4: Restic Daily Operations

Common restic operations for maintaining offsite backups.

```bash
# List all snapshots
restic snapshots
# ID        Time                 Tags        Paths
# a1b2c3d4  2026-03-21 03:15:00  daily       /home/nero/backups/...
# e5f6g7h8  2026-03-20 03:12:00  daily       /home/nero/backups/...

# Check repository integrity
restic check

# Show repository stats
restic stats
# Total Size:   2.340 GiB
# Snapshots:    15

# Show what changed between snapshots
restic diff a1b2c3d4 e5f6g7h8

# Mount snapshots as filesystem (browsable)
mkdir /tmp/restic-mount
restic mount /tmp/restic-mount &
ls /tmp/restic-mount/snapshots/latest/

# Find a specific file across snapshots
restic find "*.env"

# Restore single file from specific snapshot
restic restore e5f6g7h8 --include "/.env" --target /tmp/single-restore/
```
