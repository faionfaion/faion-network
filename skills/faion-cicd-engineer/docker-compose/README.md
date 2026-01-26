# Docker Compose Reference

**Multi-container orchestration with Docker Compose**

---

## Overview

Docker Compose is a tool for defining and running multi-container applications using a single YAML configuration file. It simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes.

## Core Components

| Component | Purpose |
|-----------|---------|
| **Services** | Computing components (containerized apps) |
| **Networks** | Inter-service communication and isolation |
| **Volumes** | Persistent data storage |
| **Configs** | Runtime configuration files |
| **Secrets** | Sensitive data (passwords, keys) |

## Modern Compose File (2025+)

The `version:` field is **obsolete**. Modern files start directly with `services:`:

```yaml
services:
  app:
    image: myapp:latest
    # ... configuration
```

## Service Configuration

### Basic Structure

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - BUILD_ENV=production
    image: myapp:latest
    container_name: myapp
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./data:/app/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Dependencies (depends_on)

### Conditions

| Condition | Use Case |
|-----------|----------|
| `service_started` | Basic startup ordering |
| `service_healthy` | Wait for healthcheck pass |
| `service_completed_successfully` | Wait for task completion |

### Advanced Options (Compose 2.20.0+)

```yaml
depends_on:
  db:
    condition: service_healthy
    restart: true      # Restart when dependency updates
    required: false    # Optional dependency (warns only)
```

## Health Checks

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `test` | Command to run | - |
| `interval` | Time between checks | 30s |
| `timeout` | Check timeout | 30s |
| `retries` | Failures before unhealthy | 3 |
| `start_period` | Grace period at startup | 0s |
| `start_interval` | Interval during start_period | 5s |

### Common Patterns

```yaml
# HTTP endpoint
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3

# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5

# Redis
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 3

# MySQL
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
```

## Networks

### Configuration

```yaml
services:
  app:
    networks:
      frontend:
      backend:
        aliases:
          - api
          - backend-service
        ipv4_address: 172.16.238.10

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.16.238.0/24
```

### Service Discovery

Containers reach each other by service name:
- `postgres://db:5432/mydb`
- `redis://cache:6379`
- `http://api:8000/v1`

## Volumes

### Types

| Type | Use Case |
|------|----------|
| Named volumes | Persistent data (databases) |
| Bind mounts | Config files, development |
| tmpfs | Ephemeral in-memory storage |

### Configuration

```yaml
services:
  app:
    volumes:
      # Named volume
      - app-data:/app/data
      # Bind mount (read-only)
      - ./config:/app/config:ro
      # Anonymous volume
      - /app/node_modules
      # tmpfs
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100m

volumes:
  app-data:
    driver: local
```

## Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
```

## Restart Policies

| Policy | Behavior |
|--------|----------|
| `no` | No automatic restart (default) |
| `always` | Always restart until removed |
| `on-failure[:max]` | Restart on failure with optional limit |
| `unless-stopped` | Restart except when explicitly stopped |

## Common Commands

```bash
# Start services
docker compose up -d

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f app

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Execute command
docker compose exec app bash

# Scale service
docker compose up -d --scale app=3

# Watch for changes (development)
docker compose watch
```

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness checklist |
| [examples.md](examples.md) | Complete compose examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts |

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/reference/compose-file/)
- [Services Reference](https://docs.docker.com/reference/compose-file/services/)
- [Docker Best Practices 2025](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/)
- [Awesome Compose (GitHub)](https://github.com/docker/awesome-compose)

---

*Docker Compose Reference | faion-cicd-engineer*
