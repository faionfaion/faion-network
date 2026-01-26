# Docker Compose Examples

**Production Patterns: Full Stack, Networking, Scaling, Security (2025-2026)**

---

## Full Stack Examples

### Python (FastAPI/Django) Stack

```yaml
# compose.yaml

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${REGISTRY:-localhost}/myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp:size=100M
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
          pids: 100
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - frontend
      - backend
    volumes:
      - app-data:/app/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app} -d ${DB_NAME:-appdb}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    # No ports - internal only

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    # No ports - internal only

  worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${REGISTRY:-localhost}/myapp:${VERSION:-latest}
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    command: celery -A app worker --loglevel=info
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
  redis-data:
  app-data:
```

### Node.js (Next.js) Stack

```yaml
# compose.yaml

services:
  app:
    build:
      context: .
      target: production
    image: ${REGISTRY:-localhost}/nextapp:${VERSION:-latest}
    container_name: nextapp
    restart: unless-stopped
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /app/.next/cache:size=500M
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=${NEXTAUTH_URL:-http://localhost:3000}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    networks:
      - frontend
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: nextapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres-data:
```

---

## Development Override

```yaml
# compose.override.yaml

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
      - /app/.venv
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: npm run dev  # or uvicorn with --reload
    ports:
      - "${APP_PORT:-8000}:8000"
      - "9229:9229"  # Debug port

  db:
    ports:
      - "${DB_PORT:-5432}:5432"

  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"

  mailhog:
    image: mailhog/mailhog
    container_name: myapp-mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - backend
    profiles:
      - dev
```

---

## Networking Examples

### Three-Tier Architecture

```yaml
# compose.yaml

services:
  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      app:
        condition: service_healthy
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  app:
    image: myapp:1.0.0
    restart: unless-stopped
    # No ports exposed - nginx only
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    # No ports exposed - app only
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Microservices with API Gateway

```yaml
# compose.yaml

services:
  gateway:
    image: kong:latest
    container_name: api-gateway
    restart: unless-stopped
    ports:
      - "8000:8000"
      - "8443:8443"
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/etc/kong/kong.yml
      - KONG_PROXY_ACCESS_LOG=/dev/stdout
      - KONG_ADMIN_ACCESS_LOG=/dev/stdout
      - KONG_PROXY_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_ERROR_LOG=/dev/stderr
    volumes:
      - ./kong/kong.yml:/etc/kong/kong.yml:ro
    networks:
      - public
      - services
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 30s
      timeout: 10s
      retries: 3

  user-service:
    build: ./services/user
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://user:${USER_DB_PASS}@user-db:5432/users
    depends_on:
      user-db:
        condition: service_healthy
    networks:
      - services
      - user-internal
    # No ports - gateway only

  order-service:
    build: ./services/order
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://order:${ORDER_DB_PASS}@order-db:5432/orders
      - USER_SERVICE_URL=http://user-service:8000
    depends_on:
      order-db:
        condition: service_healthy
    networks:
      - services
      - order-internal
    # No ports - gateway only

  user-db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=${USER_DB_PASS}
      - POSTGRES_DB=users
    volumes:
      - user-db-data:/var/lib/postgresql/data
    networks:
      - user-internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  order-db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=order
      - POSTGRES_PASSWORD=${ORDER_DB_PASS}
      - POSTGRES_DB=orders
    volumes:
      - order-db-data:/var/lib/postgresql/data
    networks:
      - order-internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U order"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  public:
    driver: bridge
  services:
    driver: bridge
  user-internal:
    driver: bridge
    internal: true
  order-internal:
    driver: bridge
    internal: true

volumes:
  user-db-data:
  order-db-data:
```

### Custom Subnet Configuration

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
```

---

## Scaling Examples

### Scalable Web Service with Nginx Load Balancer

```yaml
# compose.yaml

services:
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    networks:
      - frontend

  app:
    # No container_name - allows scaling
    build:
      context: .
      target: production
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      mode: replicated
      replicas: 3
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    networks:
      - frontend
      - backend

  db:
    image: postgres:16-alpine
    container_name: app-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres-data:
```

### Nginx Configuration for Scaling

```nginx
# nginx/nginx.conf

upstream app {
    server app:8000;
    # Docker DNS handles load balancing to replicas
}

server {
    listen 80;

    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

### Scale Command

```bash
# Scale to 5 instances
docker compose up -d --scale app=5

# Verify
docker compose ps
```

---

## Storage Examples

### Named Volumes for Databases

```yaml
services:
  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - PGDATA=/var/lib/postgresql/data/pgdata

  mysql:
    image: mysql:8
    volumes:
      - mysql-data:/var/lib/mysql

  mongodb:
    image: mongo:7
    volumes:
      - mongo-data:/data/db

volumes:
  postgres-data:
  mysql-data:
  mongo-data:
```

### Read-Only with tmpfs

```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp:size=100M,mode=1777
      - /var/run:size=10M,mode=755
    volumes:
      - ./config:/app/config:ro      # Read-only config
      - app-data:/app/data           # Writable data volume

volumes:
  app-data:
```

### Volume Backup Pattern

```yaml
# compose.yaml

services:
  backup:
    image: alpine
    volumes:
      - postgres-data:/data:ro
      - ./backups:/backup
    command: tar czf /backup/postgres-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .
    profiles:
      - backup

volumes:
  postgres-data:
```

```bash
# Run backup
docker compose --profile backup run --rm backup
```

---

## Security Examples

### Maximum Security Configuration

```yaml
services:
  app:
    image: myapp:1.0.0
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /var/run:size=10M
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port < 1024
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-profile.json
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
          pids: 100
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  app-network:
    driver: bridge
```

### Secrets Management

```yaml
services:
  app:
    image: myapp:1.0.0
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Pre-created with: docker secret create api_key key.txt
```

---

## Init Containers

### Database Migration Pattern

```yaml
services:
  migrations:
    build:
      context: .
      target: production
    command: python manage.py migrate
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    restart: "no"  # Run once

  app:
    build:
      context: .
      target: production
    depends_on:
      migrations:
        condition: service_completed_successfully
      db:
        condition: service_healthy
    networks:
      - frontend
      - backend

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
```

---

## Profiles Examples

### Environment-Specific Services

```yaml
services:
  app:
    build: .
    profiles: []  # Always starts

  # Development only
  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    profiles:
      - dev

  # Development only
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    profiles:
      - dev

  # Production only
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    profiles:
      - prod
      - monitoring

  # Production only
  grafana:
    image: grafana/grafana
    volumes:
      - grafana-data:/var/lib/grafana
    profiles:
      - prod
      - monitoring

volumes:
  grafana-data:
```

```bash
# Development
docker compose --profile dev up

# Production with monitoring
docker compose --profile prod up
docker compose --profile prod --profile monitoring up
```

---

## Logging Examples

### JSON with Rotation

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

### Centralized Logging with Loki

```yaml
services:
  app:
    logging:
      driver: "loki"
      options:
        loki-url: "http://loki:3100/loki/api/v1/push"
        loki-batch-size: "400"
        loki-retries: "3"

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  loki-data:
  grafana-data:
```

---

## Complete Production Example

### .env.example

```bash
# Application
VERSION=1.0.0
SECRET_KEY=change-me-in-production
LOG_LEVEL=info

# Ports
APP_PORT=8000

# Database
DB_USER=app
DB_PASSWORD=secure-password-here
DB_NAME=appdb

# Registry
REGISTRY=ghcr.io/org
```

### compose.yaml (Production)

See "Python (FastAPI/Django) Stack" example above.

### compose.override.yaml (Development)

See "Development Override" example above.

### compose.prod.yaml (Production Overrides)

```yaml
# compose.prod.yaml

services:
  app:
    image: ${REGISTRY}/myapp:${VERSION}
    build: null  # Use pre-built image
    restart: always
    deploy:
      mode: replicated
      replicas: 2
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s

  db:
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  redis:
    restart: always
```

### Usage

```bash
# Development
docker compose up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

---

*Docker Compose Examples | faion-infrastructure-engineer*
