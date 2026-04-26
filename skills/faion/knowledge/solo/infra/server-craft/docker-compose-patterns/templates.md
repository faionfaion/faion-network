# Docker Compose Patterns Templates

## PostgreSQL + Redis + RabbitMQ Stack

Complete infrastructure stack for a Python/Celery application platform.

```yaml
# docker-compose.yml
# Infrastructure services for application platform
# Application code runs as systemd services, not in Docker

services:
  # === PostgreSQL ===
  postgres:
    image: postgres:16-alpine
    container_name: nero-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./config/postgres/postgresql.conf:/etc/postgresql/conf.d/custom.conf:ro
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-nero}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}
      POSTGRES_DB: ${POSTGRES_DB:-nero_db}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-nero} -d ${POSTGRES_DB:-nero_db}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
        reservations:
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # === Redis ===
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
      --save 900 1
      --save 300 10
      --save 60 10000
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 768M
          cpus: "1.0"
        reservations:
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # === RabbitMQ ===
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
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-nero}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD:?RABBITMQ_PASSWORD is required}
      RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_VHOST:-nero}
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
          cpus: "1.0"
        reservations:
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # === Flower (Celery Monitor) ===
  flower:
    image: mher/flower:2.0
    container_name: nero-flower
    restart: unless-stopped
    ports:
      - "127.0.0.1:5555:5555"
    environment:
      CELERY_BROKER_URL: "amqp://${RABBITMQ_USER:-nero}:${RABBITMQ_PASSWORD}@rabbitmq:5672/${RABBITMQ_VHOST:-nero}"
      FLOWER_BASIC_AUTH: "${FLOWER_USER:-admin}:${FLOWER_PASSWORD:?FLOWER_PASSWORD is required}"
      FLOWER_PORT: 5555
      FLOWER_PERSISTENT: "true"
      FLOWER_DB: "/data/flower.db"
    volumes:
      - flower-data:/data
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
  flower-data:
    name: nero-flower-data
```

## Docker Daemon Configuration

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true,
  "default-address-pools": [
    {
      "base": "172.17.0.0/12",
      "size": 24
    }
  ],
  "features": {
    "buildkit": true
  }
}
```

Location: `/etc/docker/daemon.json`

| Setting | Purpose |
|---------|---------|
| log-driver/log-opts | Global log rotation |
| live-restore | Containers survive daemon restart |
| default-address-pools | Custom Docker network ranges |
| buildkit | Faster, more efficient builds |

## Environment File Template

```bash
# .env - Docker Compose environment variables
# chmod 600 .env && add to .gitignore

# PostgreSQL
POSTGRES_USER=nero
POSTGRES_PASSWORD=change-me-strong-password
POSTGRES_DB=nero_db

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
RABBITMQ_USER=nero
RABBITMQ_PASSWORD=change-me-strong-password
RABBITMQ_VHOST=nero

# Flower
FLOWER_USER=admin
FLOWER_PASSWORD=change-me-flower-password
```

## PostgreSQL Custom Configuration

```ini
# config/postgres/postgresql.conf
# Custom PostgreSQL settings for a 30GB RAM server

# Connection settings
max_connections = 100
superuser_reserved_connections = 3

# Memory (tuned for 30GB server running other services)
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 32MB
maintenance_work_mem = 512MB

# WAL settings
wal_buffers = 64MB
min_wal_size = 256MB
max_wal_size = 1GB

# Query planner
random_page_cost = 1.1
effective_io_concurrency = 200

# Logging
log_min_duration_statement = 1000
log_checkpoints = on
log_connections = off
log_disconnections = off
log_lock_waits = on
log_temp_files = 0
```

## Makefile for Docker Compose

```makefile
# Makefile - Docker Compose shortcuts

.PHONY: up down restart logs ps stats clean

# Start all services
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# Restart a service (usage: make restart s=postgres)
restart:
	docker compose restart $(s)

# Follow logs (usage: make logs or make logs s=postgres)
logs:
ifdef s
	docker compose logs -f $(s)
else
	docker compose logs -f
endif

# Show running containers
ps:
	docker compose ps

# Show resource usage
stats:
	docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Cleanup: remove stopped containers, unused images, build cache
clean:
	docker system prune -f
	docker volume prune -f

# Database shell
psql:
	docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Redis shell
redis-cli:
	docker compose exec redis redis-cli

# Run database migrations (adjust command for your project)
migrate:
	cd ../nero-infra && .venv/bin/alembic upgrade head

# Backup database
backup-db:
	docker compose exec -T postgres pg_dump -U $(POSTGRES_USER) -Fc $(POSTGRES_DB) > backup_$$(date +%Y%m%d_%H%M%S).dump

# Restore database (usage: make restore-db f=backup_file.dump)
restore-db:
	docker compose exec -T postgres pg_restore -U $(POSTGRES_USER) -d $(POSTGRES_DB) --clean --if-exists < $(f)
```

## Development vs Production Compose

### Base (shared)

```yaml
# docker-compose.yml (base/production)
services:
  postgres:
    image: postgres:16-alpine
    container_name: nero-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### Development Override

```yaml
# docker-compose.override.yml (auto-loaded in dev)
services:
  postgres:
    ports:
      - "5432:5432"   # Expose to all interfaces for local dev
    environment:
      POSTGRES_PASSWORD: devpassword

  pgadmin:
    image: dpage/pgadmin4
    container_name: nero-pgadmin
    ports:
      - "127.0.0.1:5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@dev.local
      PGADMIN_DEFAULT_PASSWORD: devpassword
```

### Usage

```bash
# Dev (auto-loads docker-compose.override.yml)
docker compose up -d

# Production (explicit, no override)
docker compose -f docker-compose.yml up -d

# Or use profiles to differentiate
docker compose --profile dev up -d
```

## Docker System Cleanup Cron

```bash
#!/bin/bash
# docker-cleanup.sh
# Clean up unused Docker resources
# Run weekly via cron or systemd timer

set -euo pipefail

echo "$(date) Docker cleanup starting..."

# Remove stopped containers
docker container prune -f

# Remove unused images (not used by any container)
docker image prune -f

# Remove unused build cache
docker builder prune -f --keep-storage 2G

# Report disk usage
echo "Docker disk usage after cleanup:"
docker system df

echo "$(date) Docker cleanup complete"
```
