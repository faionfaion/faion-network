# Docker Compose Patterns

Docker Compose v2 patterns for production infrastructure services on a single VPS. Covers service definitions, networking, volumes, health checks, resource limits, logging, and multi-project setups.

## Overview

For solo developer platforms, Docker Compose is ideal for running stateful infrastructure (databases, message brokers, caches) while application code runs as systemd services. This avoids the complexity of running application code in containers while getting the benefits of containerized infrastructure.

| Run In Docker | Run As systemd |
|---------------|----------------|
| PostgreSQL | Python/FastAPI apps |
| Redis | Celery workers |
| RabbitMQ | Node.js apps |
| Flower | Telegram bots |
| Monitoring tools | Custom scripts |

## Compose V2

Docker Compose V2 is a Docker CLI plugin (not a standalone binary). The command is `docker compose` (with a space, not `docker-compose`).

```bash
# V2 (current)
docker compose up -d

# V1 (legacy, deprecated)
docker-compose up -d
```

## Service Definitions

### Basic Structure

```yaml
# docker-compose.yml
services:
  service-name:
    image: postgres:16-alpine
    container_name: my-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    env_file:
      - .env

volumes:
  pgdata:
```

### Key Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| image | Container image | `postgres:16-alpine` |
| container_name | Fixed name (not generated) | `nero-postgres` |
| restart | Restart policy | `unless-stopped` |
| ports | Port mappings | `"127.0.0.1:5432:5432"` |
| volumes | Data persistence | `pgdata:/var/lib/postgresql/data` |
| environment | Env vars (inline) | `POSTGRES_PASSWORD: secret` |
| env_file | Env vars (from file) | `.env` |
| depends_on | Start ordering | See health checks section |
| command | Override CMD | `postgres -c shared_buffers=256MB` |
| entrypoint | Override ENTRYPOINT | `/custom-entrypoint.sh` |
| profiles | Optional services | `["dev", "debug"]` |

## Networking

### Default Bridge Network

Compose creates a default bridge network. Services communicate by service name.

```yaml
services:
  web:
    image: nginx
    # Can reach postgres as "postgres:5432"
  postgres:
    image: postgres:16
```

### Custom Networks

```yaml
services:
  web:
    networks:
      - frontend
      - backend
  api:
    networks:
      - backend
  postgres:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No internet access
```

### Host Network

For services that need the host's network stack:

```yaml
services:
  monitoring:
    network_mode: host
```

### Port Binding Security

Always bind to 127.0.0.1 for services that should not be publicly accessible:

```yaml
ports:
  - "127.0.0.1:5432:5432"   # Only localhost
  # NOT: "5432:5432"          # Exposes to all interfaces
```

**Warning:** Docker bypasses UFW/iptables firewall rules. A port bound to `0.0.0.0` is accessible from the internet regardless of UFW rules.

## Volumes

### Named Volumes

```yaml
volumes:
  pgdata:
    driver: local
  redis-data:
    driver: local
```

Named volumes persist data independently of containers. Location: `/var/lib/docker/volumes/`.

### Bind Mounts

```yaml
volumes:
  - ./config/postgres:/etc/postgresql/conf.d:ro  # Read-only
  - ./init-scripts:/docker-entrypoint-initdb.d    # Init scripts
```

### Volume Commands

```bash
# List volumes
docker volume ls

# Inspect a volume
docker volume inspect project_pgdata

# Remove unused volumes
docker volume prune

# Backup a volume
docker run --rm -v project_pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata.tar.gz -C /data .
```

## Health Checks

Health checks let Compose know when a service is truly ready, not just running.

```yaml
services:
  postgres:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3-management-alpine
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
```

### depends_on with Health Check

```yaml
services:
  api:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

| Condition | Meaning |
|-----------|---------|
| service_started | Container started (default) |
| service_healthy | Container started AND health check passes |
| service_completed_successfully | Container ran and exited 0 (for init tasks) |

## Resource Limits

```yaml
services:
  postgres:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
        reservations:
          memory: 512M
          cpus: "0.5"
```

| Field | Purpose |
|-------|---------|
| limits.memory | Maximum memory (container killed if exceeded) |
| limits.cpus | Maximum CPU (fractional cores) |
| reservations.memory | Guaranteed minimum memory |
| reservations.cpus | Guaranteed minimum CPU |

**Note:** `deploy.resources` works with `docker compose up` since Compose V2.

## Logging

### JSON File Driver (Default)

```yaml
services:
  postgres:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        tag: "{{.Name}}"
```

### Global Logging in daemon.json

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Location: `/etc/docker/daemon.json`. Apply with `sudo systemctl restart docker`.

### View Logs

```bash
docker compose logs postgres          # All logs for service
docker compose logs -f postgres       # Follow
docker compose logs --tail 100        # Last 100 lines
docker compose logs --since "1h"      # Last hour
```

## Profiles

Optional services that only start when explicitly requested:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    # No profile = always starts

  flower:
    image: mher/flower
    profiles: ["monitoring"]
    # Only starts with: docker compose --profile monitoring up

  pgadmin:
    image: dpage/pgadmin4
    profiles: ["dev"]
    # Only starts with: docker compose --profile dev up
```

```bash
# Start default services only
docker compose up -d

# Start with monitoring profile
docker compose --profile monitoring up -d

# Start with multiple profiles
docker compose --profile monitoring --profile dev up -d
```

## Environment Variables

### Precedence (highest to lowest)

1. Shell environment variables
2. `.env` file in same directory as docker-compose.yml
3. `env_file` directive
4. `environment` directive defaults

### .env File for Compose Interpolation

```bash
# .env (same directory as docker-compose.yml)
POSTGRES_VERSION=16
POSTGRES_PASSWORD=mysecret
```

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:${POSTGRES_VERSION}-alpine
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

### env_file for Container Environment

```yaml
services:
  api:
    env_file:
      - .env           # Default
      - .env.local      # Overrides (gitignored)
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services (detached) |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop, remove containers AND volumes |
| `docker compose ps` | List running containers |
| `docker compose logs -f` | Follow all logs |
| `docker compose restart postgres` | Restart specific service |
| `docker compose pull` | Pull latest images |
| `docker compose exec postgres psql -U nero` | Execute command in container |
| `docker compose config` | Validate and show final config |
| `docker compose top` | Show running processes |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Port already in use | Another process on same port | `ss -tlnp \| grep PORT` to find it |
| Volume permission denied | Container runs as different UID | Set user or fix permissions |
| Container keeps restarting | Application crash | `docker compose logs service-name` |
| Slow startup | No health check, depends_on wrong | Add health checks with conditions |
| Docker bypasses firewall | Docker manipulates iptables directly | Bind to 127.0.0.1 |
| Disk full | Log files or volumes | Configure log rotation, prune |

## Related Methodologies

- `systemd-user-services/` -- running applications alongside Docker infrastructure
- `backup-recovery/` -- backing up Docker volumes
- `monitoring-logging/` -- monitoring Docker containers
