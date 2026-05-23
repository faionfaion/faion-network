# purpose: Daily backup orchestrator: pg_dump + verify + Redis + configs + restic + retention.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

#!/usr/bin/env bash
# Run daily from cron at 03:00.
set -euo pipefail

BACKUP_ROOT=/home/nero/backups
STAMP=$(date +%Y%m%d)

# 1. Postgres
docker exec -t nero-postgres pg_dump -U nero -Fc nero_db \
  > "$BACKUP_ROOT/database/nero_db_${STAMP}.dump"
pg_restore --list "$BACKUP_ROOT/database/nero_db_${STAMP}.dump" >/dev/null \
  || { echo CORRUPT; exit 1; }

# 2. Redis RDB
docker cp nero-redis:/data/dump.rdb "$BACKUP_ROOT/redis/dump_${STAMP}.rdb"

# 3. Configs
tar -czf "$BACKUP_ROOT/configs/configs_${STAMP}.tgz" /etc/nginx /etc/systemd /etc/wireguard

# 4. Restic offsite + retention
export RESTIC_PASSWORD_FILE=/root/.restic-password
restic backup "$BACKUP_ROOT" --tag daily --quiet
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune --quiet

# 5. Local retention
find "$BACKUP_ROOT" -mtime +14 -delete
