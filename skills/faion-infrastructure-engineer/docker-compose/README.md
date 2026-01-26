# Docker Compose

**Multi-Container Orchestration for Modern Applications (2025-2026)**

---

## Overview

Docker Compose defines and runs multi-container applications with declarative YAML configuration. This skill covers production-grade Compose patterns: service configuration, networking, volumes, scaling, and deployment best practices.

---

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness and configuration checklists |
| [examples.md](examples.md) | Full stack patterns, networking, scaling examples |
| [templates.md](templates.md) | Ready-to-use Compose configurations |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Compose tasks |

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Service** | Container definition with image, ports, volumes, networks |
| **Network** | Communication layer between containers |
| **Volume** | Persistent storage for container data |
| **Secret** | Sensitive data (passwords, keys) managed securely |
| **Config** | Non-sensitive configuration files |
| **Profile** | Environment-specific service groups |

---

## Modern Compose (2025-2026)

### File Naming

```bash
# Modern (recommended)
compose.yaml
docker compose up

# Legacy (still supported)
docker-compose.yml
docker-compose up
```

### No Version Field

The `version:` field is obsolete. Start directly with `services:`.

```yaml
# Modern (2025-2026)
services:
  app:
    image: myapp:1.0.0

# Legacy (deprecated)
version: "3.9"
services:
  app:
    image: myapp:1.0.0
```

### New CLI

```bash
# Modern
docker compose up
docker compose down
docker compose logs

# Legacy
docker-compose up
docker-compose down
docker-compose logs
```

---

## Minimal Compose File

```yaml
# compose.yaml

services:
  app:
    image: myapp:1.0.0
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

---

## Key Features

### 1. Service Health Checks

Health checks enable dependency ordering and container recovery.

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      start_period: 40s
      retries: 3
    depends_on:
      db:
        condition: service_healthy
```

### 2. Network Isolation

Separate frontend and backend networks for security.

```yaml
services:
  nginx:
    networks:
      - frontend

  app:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### 3. Named Volumes

Persistent data storage with named volumes.

```yaml
services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
    driver: local
```

### 4. Resource Limits

Prevent resource exhaustion with limits.

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
```

### 5. Security Hardening

Production security settings.

```yaml
services:
  app:
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
```

---

## Service Configuration

### Build vs Image

```yaml
services:
  # Use pre-built image
  app-prod:
    image: ghcr.io/org/myapp:v1.0.0

  # Build from Dockerfile
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
      args:
        - NODE_ENV=development
```

### Environment Variables

```yaml
services:
  app:
    environment:
      - NODE_ENV=production
      - API_KEY=${API_KEY}  # From .env file
    env_file:
      - .env
      - .env.local
```

### Ports

```yaml
services:
  app:
    ports:
      - "8000:8000"           # host:container
      - "127.0.0.1:9000:9000" # localhost only
      - "3000"                # random host port
```

### Commands and Entrypoints

```yaml
services:
  app:
    entrypoint: ["/docker-entrypoint.sh"]
    command: ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

  worker:
    command: celery -A app worker --loglevel=info
```

---

## Dependencies

### Dependency Conditions

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy      # Wait for healthy
      redis:
        condition: service_started      # Wait for started
      migrations:
        condition: service_completed_successfully  # Wait for completion
```

### Init Containers (2025-2026)

```yaml
services:
  migrations:
    image: myapp:1.0.0
    command: python manage.py migrate
    depends_on:
      db:
        condition: service_healthy
    restart: "no"  # Run once

  app:
    depends_on:
      migrations:
        condition: service_completed_successfully
```

---

## Networking

### Network Types

| Type | Use Case |
|------|----------|
| `bridge` | Container-to-container on same host (default) |
| `host` | Container uses host network (no isolation) |
| `none` | No networking |
| `overlay` | Multi-host (Swarm mode) |

### DNS Resolution

Services reach each other by service name:

```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgres://db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
```

### Network Aliases

```yaml
services:
  app:
    networks:
      backend:
        aliases:
          - api
          - backend-api
```

### Custom Subnet

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

---

## Volumes

### Volume Types

| Type | Syntax | Use Case |
|------|--------|----------|
| Named | `data:/app/data` | Persistent data |
| Bind | `./src:/app/src` | Development |
| tmpfs | `tmpfs: /tmp` | Temporary |
| Secret | `/run/secrets/*` | Sensitive data |

### Read-Only and tmpfs

```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /var/run:size=10M
    volumes:
      - ./config:/app/config:ro  # Read-only config
      - app-data:/app/data       # Writable data
```

### Volume Configuration

```yaml
volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      device: /mnt/data/postgres
      o: bind
```

---

## Scaling

### Remove container_name for Scaling

```yaml
services:
  app:
    # container_name: myapp  # Remove this
    image: myapp:1.0.0
```

```bash
docker compose up -d --scale app=3
```

### Deploy Replicas (Swarm/Compose with Docker Desktop)

```yaml
services:
  app:
    deploy:
      mode: replicated
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s
```

---

## Profiles

Environment-specific service groups.

```yaml
services:
  app:
    profiles: []  # Always starts

  mailhog:
    image: mailhog/mailhog
    profiles:
      - dev

  monitoring:
    image: prometheus:latest
    profiles:
      - prod
      - monitoring
```

```bash
# Start only default services
docker compose up

# Start with dev profile
docker compose --profile dev up

# Start with multiple profiles
docker compose --profile dev --profile monitoring up
```

---

## Multiple Compose Files

### File Hierarchy

```bash
compose.yaml           # Base configuration
compose.override.yaml  # Auto-loaded, dev settings
compose.prod.yaml      # Production overrides
compose.test.yaml      # Test configuration
```

### Merge Strategy

```bash
# Development (auto-merges override)
docker compose up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up

# Testing
docker compose -f compose.yaml -f compose.test.yaml up
```

### Override Example

```yaml
# compose.override.yaml (development)
services:
  app:
    build:
      target: development
    volumes:
      - .:/app
    environment:
      - DEBUG=true
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port

  db:
    ports:
      - "5432:5432"  # Expose for local tools
```

---

## Logging

### Log Drivers

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        compress: "true"
```

### External Logging (Production)

```yaml
services:
  app:
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "docker.{{.Name}}"

  # Alternative: Loki
  app-loki:
    logging:
      driver: "loki"
      options:
        loki-url: "http://loki:3100/loki/api/v1/push"
```

---

## Secrets (Swarm Mode)

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

---

## Quick Commands

```bash
# Start services
docker compose up -d

# Start with build
docker compose up -d --build

# Start specific services
docker compose up -d app db

# View logs
docker compose logs -f
docker compose logs -f app

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# View running services
docker compose ps

# Execute command
docker compose exec app sh
docker compose exec db psql -U postgres

# Scale service
docker compose up -d --scale app=3

# Validate configuration
docker compose config

# View resource usage
docker compose top
docker stats
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Service can't connect to db | Check network membership, use service name |
| Volume permissions | Match container user UID with host |
| Port already in use | Change host port or stop conflicting service |
| Health check failing | Check endpoint, increase start_period |
| Dependency not healthy | Check depends_on condition, health check |

### Diagnostic Commands

```bash
# Check network
docker compose exec app ping db
docker compose exec app nslookup db

# Check health
docker inspect --format='{{json .State.Health}}' container_name

# Check logs
docker compose logs --tail 100 service_name

# Validate compose file
docker compose config --quiet
```

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| `version:` field | Obsolete, adds clutter | Remove entirely |
| `docker-compose.yml` | Old naming | Use `compose.yaml` |
| No health checks | Silent failures | Add healthcheck to all services |
| Default bridge | No isolation | Define custom networks |
| Bind mounts in prod | Security, portability | Use named volumes |
| No resource limits | Resource exhaustion | Set memory/CPU limits |
| Hardcoded secrets | Security risk | Use env_file or secrets |
| container_name + scaling | Can't scale | Remove container_name |

---

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Compose File Services](https://docs.docker.com/reference/compose-file/services/)
- [Compose File Volumes](https://docs.docker.com/reference/compose-file/volumes/)
- [Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/)
- [10 Best Practices for Docker Compose](https://dev.to/wallacefreitas/10-best-practices-for-writing-maintainable-docker-compose-files-4ca2)
- [Docker Compose Advanced Management](https://www.owais.io/blog/2025-10-03_docker-compose-advanced-management-part2)
- [Docker Best Practices 2025](https://docs.benchhub.co/docs/tutorials/docker/docker-best-practices-2025)

---

*Docker Compose | faion-infrastructure-engineer*
