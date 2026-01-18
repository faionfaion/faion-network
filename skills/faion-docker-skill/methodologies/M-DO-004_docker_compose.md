# M-DO-004: Docker Compose

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #docker, #compose, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Multi-container applications are hard to manage with plain Docker. Running separate commands for each service is error-prone and doesn't capture service relationships.

## Promise

After this methodology, you will orchestrate multi-container applications with Docker Compose. Development environments will start with a single command.

## Overview

Docker Compose defines multi-container applications in YAML. It manages networking, volumes, and service dependencies automatically.

---

## Framework

### Step 1: Basic Compose File

```yaml
# docker-compose.yml (or compose.yaml)
version: "3.9"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Step 2: Compose Commands

```bash
# Start services
docker compose up
docker compose up -d              # Detached mode
docker compose up --build         # Rebuild images

# Stop services
docker compose down               # Stop and remove
docker compose down -v            # Also remove volumes

# Service management
docker compose ps                 # List services
docker compose logs               # View logs
docker compose logs -f app        # Follow specific service

# Execute commands
docker compose exec app sh        # Shell in running container
docker compose run app npm test   # Run one-off command

# Scaling
docker compose up -d --scale worker=3
```

### Step 3: Build Configuration

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
      args:
        - NODE_ENV=development
        - VERSION=1.0.0
      target: development
      cache_from:
        - myapp:cache

    # Or simple form
    # build: .
    # build: ./path/to/dir
```

### Step 4: Networking

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    networks:
      - frontend_net

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    networks:
      - frontend_net
      - backend_net

  db:
    image: postgres:16-alpine
    networks:
      - backend_net

networks:
  frontend_net:
    driver: bridge
  backend_net:
    driver: bridge
    internal: true  # No external access
```

### Step 5: Volumes and Bind Mounts

```yaml
services:
  app:
    volumes:
      # Bind mount for development (hot reload)
      - ./src:/app/src
      - ./package.json:/app/package.json

      # Named volume for dependencies
      - node_modules:/app/node_modules

      # Read-only config
      - ./config:/app/config:ro

  db:
    volumes:
      # Named volume for persistence
      - postgres_data:/var/lib/postgresql/data

      # Init scripts
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  node_modules:
  postgres_data:
```

### Step 6: Health Checks and Dependencies

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Templates

### Full-Stack Development

```yaml
# docker-compose.yml
version: "3.9"

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    environment:
      - VITE_API_URL=http://localhost:8080
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    volumes:
      - ./backend:/app
      - backend_modules:/app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

volumes:
  postgres_data:
  redis_data:
  backend_modules:
```

### Production with Override

```yaml
# docker-compose.yml (base)
version: "3.9"

services:
  app:
    image: myapp:latest
    restart: unless-stopped
    environment:
      - NODE_ENV=production

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```yaml
# docker-compose.override.yml (development, auto-loaded)
version: "3.9"

services:
  app:
    build: .
    volumes:
      - ./src:/app/src
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development

  db:
    ports:
      - "5432:5432"
```

```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    # No exposed ports in production
```

```bash
# Development (uses base + override)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Environment Files

```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env
      - .env.local
    environment:
      # Override specific vars
      - LOG_LEVEL=debug
```

```bash
# .env
DATABASE_URL=postgres://user:pass@db:5432/mydb
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key

# .env.local (not committed)
SECRET_KEY=override-for-local
```

---

## Examples

### Database Migrations

```yaml
services:
  migrate:
    build: .
    command: npm run migrate
    depends_on:
      db:
        condition: service_healthy
    profiles:
      - tools

  seed:
    build: .
    command: npm run seed
    depends_on:
      - migrate
    profiles:
      - tools
```

```bash
# Run migrations
docker compose --profile tools run migrate

# Run seeds
docker compose --profile tools run seed
```

### Multiple Environments

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:${TAG:-latest}
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
```

```bash
# .env.staging
TAG=staging
DATABASE_URL=postgres://staging-db/mydb
REDIS_URL=redis://staging-redis

# .env.production
TAG=v1.2.3
DATABASE_URL=postgres://prod-db/mydb
REDIS_URL=redis://prod-redis

# Run with specific env
docker compose --env-file .env.staging up
```

---

## Common Mistakes

1. **Not using named volumes** - Data lost on container remove
2. **Missing depends_on** - Services start in wrong order
3. **Hardcoded secrets** - Use env_file or secrets
4. **No health checks** - depends_on doesn't wait for ready
5. **Exposing all ports** - Only expose what's needed

---

## Checklist

- [ ] Named volumes for persistence
- [ ] Health checks for databases
- [ ] depends_on with conditions
- [ ] Override files for environments
- [ ] .env files for secrets
- [ ] Network isolation
- [ ] Resource limits defined
- [ ] Restart policies set

---

## Next Steps

- M-DO-003: Docker Basics
- M-DO-005: Kubernetes Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-004 v1.0*
