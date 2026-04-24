# Docker Compose Templates

Copy-paste templates for common configurations.

## Base Service Template

```yaml
services:
  app:
    image: ${IMAGE_NAME}:${VERSION:-latest}
    container_name: ${PROJECT_NAME}-app
    restart: unless-stopped
    ports:
      - "${HOST_PORT}:${CONTAINER_PORT}"
    environment:
      - ENV_VAR=${ENV_VAR}
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${CONTAINER_PORT}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - default
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Database Templates

### PostgreSQL

```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: ${PROJECT_NAME}-db
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
          memory: 256M

volumes:
  postgres-data:
```

### MySQL

```yaml
services:
  db:
    image: mysql:8
    container_name: ${PROJECT_NAME}-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME:-appdb}
      - MYSQL_USER=${DB_USER:-app}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
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

volumes:
  mysql-data:
```

### MongoDB

```yaml
services:
  mongo:
    image: mongo:7
    container_name: ${PROJECT_NAME}-mongo
    restart: unless-stopped
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_USER:-admin}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
      - MONGO_INITDB_DATABASE=${MONGO_DB:-appdb}
    volumes:
      - mongo-data:/data/db
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
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

volumes:
  mongo-data:
```

## Cache Templates

### Redis

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: ${PROJECT_NAME}-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory ${REDIS_MAXMEM:-100mb} --maxmemory-policy allkeys-lru
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

volumes:
  redis-data:
```

### Memcached

```yaml
services:
  memcached:
    image: memcached:alpine
    container_name: ${PROJECT_NAME}-memcached
    restart: unless-stopped
    command: memcached -m 64
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "11211"]
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
```

## Message Queue Templates

### RabbitMQ

```yaml
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: ${PROJECT_NAME}-rabbitmq
    restart: unless-stopped
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER:-guest}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASSWORD:-guest}
    ports:
      - "15672:15672"  # Management UI (remove in production)
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

volumes:
  rabbitmq-data:
```

## Reverse Proxy Templates

### Nginx

```yaml
services:
  nginx:
    image: nginx:alpine
    container_name: ${PROJECT_NAME}-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
      - static-files:/var/www/static:ro
    depends_on:
      - app
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  static-files:
```

### Traefik

```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: ${PROJECT_NAME}-traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/letsencrypt
    networks:
      - frontend
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.${DOMAIN}`)"
      - "traefik.http.routers.dashboard.service=api@internal"

volumes:
  traefik-certs:
```

## Worker Template

```yaml
services:
  worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${IMAGE_NAME}:${VERSION:-latest}
    container_name: ${PROJECT_NAME}-worker
    restart: unless-stopped
    command: ${WORKER_COMMAND}
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
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
    profiles:
      - worker
```

## Network Template

```yaml
networks:
  frontend:
    driver: bridge
    name: ${PROJECT_NAME}-frontend
  backend:
    driver: bridge
    internal: true
    name: ${PROJECT_NAME}-backend
```

## Volume Template

```yaml
volumes:
  postgres-data:
    name: ${PROJECT_NAME}-postgres-data
  redis-data:
    name: ${PROJECT_NAME}-redis-data
  app-data:
    name: ${PROJECT_NAME}-app-data
```

## Environment File Template

`.env.example`:

```bash
# Project
PROJECT_NAME=myapp
VERSION=1.0.0

# Application
SECRET_KEY=change-me-in-production
LOG_LEVEL=info
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_USER=app
DB_PASSWORD=secure-password-here
DB_NAME=appdb
DB_ROOT_PASSWORD=root-password-here

# Redis
REDIS_MAXMEM=100mb

# MongoDB
MONGO_USER=admin
MONGO_PASSWORD=mongo-password-here
MONGO_DB=appdb

# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Traefik/SSL
DOMAIN=example.com
ACME_EMAIL=admin@example.com

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# External Services
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=smtp-password

# Feature Flags
ENABLE_FEATURE_X=false
```

## Watch Template (2025)

```yaml
services:
  app:
    develop:
      watch:
        # Sync source files without restart
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - node_modules/
            - __pycache__/

        # Rebuild on dependency changes
        - action: rebuild
          path: package.json
        - action: rebuild
          path: requirements.txt

        # Sync config and restart
        - action: sync+restart
          path: ./config
          target: /app/config
```

## Profiles Template

```yaml
services:
  # Always started
  app:
    # ...

  db:
    # ...

  # Development tools
  mailhog:
    image: mailhog/mailhog
    profiles:
      - dev

  adminer:
    image: adminer
    profiles:
      - dev

  # Worker services
  worker:
    profiles:
      - worker

  scheduler:
    profiles:
      - worker

  # Monitoring
  prometheus:
    profiles:
      - monitoring

  grafana:
    profiles:
      - monitoring
```

Usage:
```bash
docker compose up -d                      # Core services only
docker compose --profile dev up -d        # Core + dev tools
docker compose --profile worker up -d     # Core + workers
docker compose --profile dev --profile monitoring up -d  # Multiple profiles
```

## Secrets Template (Docker Swarm)

```yaml
services:
  app:
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
    external: true
    name: my_api_key
```
