# Docker Compose Reference

**Multi-container orchestration with Docker Compose**

---

## Basic Configuration

```yaml
# docker-compose.yml
version: "3.9"

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
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
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

  db:
    image: postgres:15-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network

volumes:
  db_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

---

## Development vs Production

```yaml
# docker-compose.yml (base)
version: "3.9"

services:
  app:
    build: .
    networks:
      - app-network

networks:
  app-network:
```

```yaml
# docker-compose.override.yml (development, auto-loaded)
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - DEBUG=true
    command: npm run dev
```

```yaml
# docker-compose.prod.yml (production)
version: "3.9"

services:
  app:
    build:
      target: production
    restart: unless-stopped
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
```

**Usage:**
```bash
# Development (uses override automatically)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Service Dependencies

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      migrations:
        condition: service_completed_successfully

  migrations:
    build: .
    command: python manage.py migrate
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 5
```

---

## DNS and Service Discovery

```yaml
# docker-compose.yml
services:
  app:
    networks:
      app-network:
        aliases:
          - api
          - backend

  db:
    networks:
      app-network:

networks:
  app-network:
```

Containers can reach each other by service name: `postgres://db:5432/mydb`

---

## Volume Management

```yaml
services:
  app:
    volumes:
      # Named volume
      - app-data:/app/data
      # Bind mount
      - ./config:/app/config:ro
      # Anonymous volume (preserved on rebuild)
      - /app/node_modules
      # tmpfs (in-memory)
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100m

volumes:
  app-data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
```

---

## Secrets Management

```yaml
# docker-compose.yml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Created via: docker secret create api_key key.txt
```

**Access in container:** `/run/secrets/db_password`

---

## Secure Compose Example

```yaml
services:
  app:
    image: myapp:v1.0.0
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          cpus: "0.25"
          memory: 128M
```

---

## Healthchecks in Compose

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

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

# Execute command in running service
docker compose exec app bash

# Scale service
docker compose up -d --scale app=3
```

---

## Production Checklist

- [ ] Image tagged with version
- [ ] Health checks configured
- [ ] Logging to stdout/stderr
- [ ] Graceful shutdown handled
- [ ] Environment variables documented
- [ ] Resource limits defined
- [ ] Restart policy set

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Awesome Compose (GitHub)](https://github.com/docker/awesome-compose)
- [Docker Security](https://docs.docker.com/engine/security/)
