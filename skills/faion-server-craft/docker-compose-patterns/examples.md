# Docker Compose Patterns Examples

## Example 1: NERO Infrastructure Stack

The NERO platform runs PostgreSQL, Redis, RabbitMQ, and Flower in Docker Compose. Application services (Celery workers, FastAPI, React SPA) run as systemd user services.

### Architecture

```
Docker Compose (infrastructure):
  - postgres:16-alpine    -> 127.0.0.1:5432
  - redis:7-alpine        -> 127.0.0.1:6379
  - rabbitmq:3-management -> 127.0.0.1:5672, 127.0.0.1:15672
  - flower:2.0            -> 127.0.0.1:5555

systemd user services (applications):
  - nero-core (Celery)    -> connects to all Docker services
  - nero-channel-web      -> 127.0.0.1:8100
  - nero-channel-tg       -> connects to RabbitMQ
  - nero-web              -> 127.0.0.1:8101
  - nero-beat             -> connects to RabbitMQ
  - nero-autoheal         -> monitors all services
```

### docker-compose.yml

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: nero-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    env_file: .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    command: >
      postgres
      -c shared_buffers=2GB
      -c effective_cache_size=6GB
      -c work_mem=32MB
      -c maintenance_work_mem=512MB
      -c max_connections=100
      -c wal_buffers=64MB
      -c random_page_cost=1.1
      -c effective_io_concurrency=200
      -c log_min_duration_statement=1000
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "4.0"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: nero-redis
    restart: unless-stopped
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis-data:/data
    command: >
      redis-server
      --appendonly yes
      --appendfsync everysec
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 768M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: nero-rabbitmq
    restart: unless-stopped
    ports:
      - "127.0.0.1:5672:5672"
      - "127.0.0.1:15672:15672"
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
      RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_VHOST}
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 1G
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  flower:
    image: mher/flower:2.0
    container_name: nero-flower
    restart: unless-stopped
    ports:
      - "127.0.0.1:5555:5555"
    environment:
      CELERY_BROKER_URL: "amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@rabbitmq:5672/${RABBITMQ_VHOST}"
      FLOWER_BASIC_AUTH: "${FLOWER_USER}:${FLOWER_PASSWORD}"
    depends_on:
      rabbitmq:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "5m"
        max-file: "2"

volumes:
  pgdata:
    name: nero-pgdata
  redis-data:
    name: nero-redis-data
  rabbitmq-data:
    name: nero-rabbitmq-data
```

### Daily Operations

```bash
# Start infrastructure
cd ~/workspace/repos/nero-infra
docker compose up -d

# Check all services are healthy
docker compose ps
# NAME              STATUS                  PORTS
# nero-postgres     Up 5 days (healthy)     127.0.0.1:5432->5432/tcp
# nero-redis        Up 5 days (healthy)     127.0.0.1:6379->6379/tcp
# nero-rabbitmq     Up 5 days (healthy)     127.0.0.1:5672->5672/tcp
# nero-flower       Up 5 days              127.0.0.1:5555->5555/tcp

# Quick database access
docker compose exec postgres psql -U nero -d nero_db

# Monitor resource usage
docker stats --no-stream
# NAME             CPU %   MEM USAGE / LIMIT   NET I/O
# nero-postgres    2.5%    385MiB / 4GiB       15GB / 12GB
# nero-redis       0.1%    45MiB / 768MiB      8GB / 6GB
# nero-rabbitmq    1.2%    180MiB / 1GiB       20GB / 18GB
# nero-flower      0.3%    85MiB / 256MiB      500MB / 200MB

# Update PostgreSQL (minor version)
docker compose pull postgres
docker compose up -d postgres
# Data persists in pgdata volume
```

---

## Example 2: Multi-Project Docker Networking

Running multiple projects on the same server, each with their own database but sharing common infrastructure.

### Project Layout

```
/srv/nero/nero-infra/docker-compose.yml      # NERO platform infra
/srv/meetingtax/docker-compose.yml            # MeetingTax project infra
```

### Shared Network Approach

```yaml
# NERO infra docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    container_name: nero-postgres
    networks:
      - shared-infra
    # One PostgreSQL instance, multiple databases

networks:
  shared-infra:
    name: shared-infra
    driver: bridge
```

```yaml
# MeetingTax docker-compose.yml
services:
  meetingtax-api:
    image: meetingtax-api:latest
    networks:
      - shared-infra
    environment:
      DATABASE_URL: postgresql://meetingtax:pass@nero-postgres:5432/meetingtax_db

networks:
  shared-infra:
    external: true  # Use network created by NERO
```

### Separate Databases in Shared PostgreSQL

```bash
# Create database for new project
docker compose exec postgres psql -U nero -c "
  CREATE USER meetingtax WITH PASSWORD 'secure-password';
  CREATE DATABASE meetingtax_db OWNER meetingtax;
  GRANT ALL PRIVILEGES ON DATABASE meetingtax_db TO meetingtax;
"
```

---

## Example 3: PostgreSQL Major Version Upgrade

Upgrading PostgreSQL from 15 to 16 with data migration.

```bash
# 1. Backup current database
docker compose exec -T postgres pg_dumpall -U nero > pg15_full_backup.sql

# 2. Also create per-database custom format backup
docker compose exec -T postgres pg_dump -U nero -Fc nero_db > nero_db_pg15.dump

# 3. Stop the old container
docker compose stop postgres

# 4. Rename old volume (keep as safety net)
docker volume create nero-pgdata-pg15-backup
docker run --rm \
  -v nero-pgdata:/source:ro \
  -v nero-pgdata-pg15-backup:/backup \
  alpine sh -c "cp -a /source/. /backup/"

# 5. Remove old volume
docker compose down -v  # WARNING: removes all volumes
# Or specifically:
docker volume rm nero-pgdata

# 6. Update image version in docker-compose.yml
# Change: image: postgres:15-alpine
# To:     image: postgres:16-alpine

# 7. Start with new version (creates fresh volume)
docker compose up -d postgres

# 8. Wait for health check
docker compose ps  # Wait for "healthy"

# 9. Restore data
cat pg15_full_backup.sql | docker compose exec -T postgres psql -U nero

# 10. Verify
docker compose exec postgres psql -U nero -d nero_db -c "SELECT version();"
docker compose exec postgres psql -U nero -d nero_db -c "SELECT count(*) FROM some_table;"

# 11. Clean up backup volume (after confirming everything works)
# docker volume rm nero-pgdata-pg15-backup
```

---

## Example 4: Docker Volume Backup Script

```bash
#!/bin/bash
# backup-docker-volumes.sh
# Backup all named Docker volumes used by the project

set -euo pipefail

BACKUP_DIR="/home/nero/backups/docker-volumes"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

echo "=== Docker Volume Backup - $DATE ==="

# List of volumes to backup
VOLUMES=(
    "nero-pgdata"
    "nero-redis-data"
    "nero-rabbitmq-data"
)

for vol in "${VOLUMES[@]}"; do
    echo "Backing up: $vol"

    # Check volume exists
    if ! docker volume inspect "$vol" &>/dev/null; then
        echo "  WARNING: Volume $vol not found, skipping"
        continue
    fi

    BACKUP_FILE="$BACKUP_DIR/${vol}_${DATE}.tar.gz"

    # Create backup using a temporary alpine container
    docker run --rm \
        -v "$vol":/data:ro \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf "/backup/${vol}_${DATE}.tar.gz" -C /data .

    SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    echo "  Done: $BACKUP_FILE ($SIZE)"
done

# Clean up old backups
echo ""
echo "Cleaning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +"$RETENTION_DAYS" -delete

echo ""
echo "Current backups:"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -20

echo ""
echo "Total backup size: $(du -sh "$BACKUP_DIR" | cut -f1)"
```

---

## Example 5: Health Check Dashboard

A simple script to display Docker service health alongside systemd services.

```bash
#!/bin/bash
# service-health.sh
# Combined health check for Docker + systemd services

echo "=== Infrastructure (Docker) ==="
printf "%-20s %-12s %-15s %s\n" "SERVICE" "STATUS" "HEALTH" "UPTIME"

docker compose -f /srv/nero/nero-infra/docker-compose.yml ps --format json 2>/dev/null | \
    python3 -c "
import sys, json
for line in sys.stdin:
    s = json.loads(line)
    name = s.get('Name', 'unknown')
    state = s.get('State', 'unknown')
    health = s.get('Health', 'n/a')
    status = s.get('Status', '')
    print(f'{name:<20} {state:<12} {health:<15} {status}')
" 2>/dev/null || echo "  (Docker Compose not running or not accessible)"

echo ""
echo "=== Applications (systemd) ==="
printf "%-20s %-12s %-15s %s\n" "SERVICE" "STATUS" "MEMORY" "PID"

for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal; do
    status=$(systemctl --user is-active "$svc" 2>/dev/null || echo "unknown")
    memory=$(systemctl --user show "$svc" --property=MemoryCurrent 2>/dev/null | cut -d= -f2)
    pid=$(systemctl --user show "$svc" --property=MainPID 2>/dev/null | cut -d= -f2)

    # Convert memory to MB
    if [ -n "$memory" ] && [ "$memory" != "[not set]" ] && [ "$memory" != "infinity" ]; then
        memory_mb=$((memory / 1048576))M
    else
        memory_mb="n/a"
    fi

    printf "%-20s %-12s %-15s %s\n" "$svc" "$status" "$memory_mb" "$pid"
done
```
