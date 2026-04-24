# Docker Compose Templates

**Copy-paste templates for common scenarios**

---

## Service Templates

### Basic Service

```yaml
services:
  myservice:
    image: myimage:1.0.0
    container_name: myservice
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - ENV_VAR=value
    env_file:
      - .env
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
```

### Build from Dockerfile

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - BUILD_ENV=production
    image: myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
```

### Secure Service

```yaml
services:
  app:
    image: myapp:1.0.0
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
```

---

## Database Templates

### PostgreSQL

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME:-mydb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres} -d ${DB_NAME:-mydb}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

volumes:
  postgres-data:
```

### MySQL

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME:-mydb}
      MYSQL_USER: ${DB_USER:-app}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 60s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

volumes:
  mysql-data:
```

### MongoDB

```yaml
services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
      MONGO_INITDB_DATABASE: ${DB_NAME:-mydb}
    volumes:
      - mongodb-data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

volumes:
  mongodb-data:
```

---

## Cache Templates

### Redis

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 256M

volumes:
  redis-data:
```

### Memcached

```yaml
services:
  memcached:
    image: memcached:1.6-alpine
    container_name: memcached
    restart: unless-stopped
    command: memcached -m 256
    networks:
      - backend
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "11211"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 256M
```

---

## Web Server Templates

### Nginx Reverse Proxy

```yaml
services:
  nginx:
    image: nginx:1.25-alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
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
```

### Traefik

```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/dynamic:/etc/traefik/dynamic:ro
      - traefik-certs:/letsencrypt
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "traefik", "healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  traefik-certs:
```

---

## Queue Templates

### RabbitMQ

```yaml
services:
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: rabbitmq
    restart: unless-stopped
    ports:
      - "5672:5672"
      - "15672:15672"  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-guest}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    networks:
      - backend
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

volumes:
  rabbitmq-data:
```

---

## Network Templates

### Basic Network

```yaml
networks:
  app-network:
    driver: bridge
```

### Multi-Tier Networks

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Custom Subnet

```yaml
networks:
  custom-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

---

## Volume Templates

### Named Volume

```yaml
volumes:
  app-data:
    driver: local
```

### External Volume

```yaml
volumes:
  shared-data:
    external: true
    name: my-external-volume
```

### Local Path Volume

```yaml
volumes:
  host-data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
```

---

## Depends_on Templates

### With Health Check

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
```

### With Migration

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully

  migrations:
    command: python manage.py migrate
    depends_on:
      db:
        condition: service_healthy
    restart: "no"
```

### Optional Dependency

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
        required: false  # Warns but continues if unavailable
```

---

## Health Check Templates

### HTTP

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

### TCP Port

```yaml
healthcheck:
  test: ["CMD", "nc", "-z", "localhost", "8080"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Shell Command

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Disable (Override Image Default)

```yaml
healthcheck:
  disable: true
```

---

## Environment Templates

### .env File

```bash
# .env
# Database
DB_USER=myuser
DB_PASSWORD=secretpassword
DB_NAME=mydb

# Application
NODE_ENV=production
API_KEY=your-api-key

# Versions
VERSION=1.0.0
```

### Multiple Environments

```yaml
services:
  app:
    env_file:
      - .env
      - .env.${ENVIRONMENT:-development}
    environment:
      - NODE_ENV=${ENVIRONMENT:-development}
```

---

## Full Project Template

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - app-uploads:/app/uploads
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  db-data:
  redis-data:
  app-uploads:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

---

*Docker Compose Templates | faion-cicd-engineer*
