# Docker Compose Examples

**Complete, production-ready compose configurations**

---

## Example 1: Full-Stack Web Application

Node.js API with PostgreSQL, Redis, and Nginx reverse proxy.

```yaml
services:
  nginx:
    image: nginx:1.25-alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
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

  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:${VERSION:-latest}
    container_name: myapp-api
    restart: unless-stopped
    expose:
      - "3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:${DB_PASSWORD}@db:5432/mydb
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
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
        reservations:
          cpus: "0.5"
          memory: 512M

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
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

## Example 2: Django Application with Celery

Django API with PostgreSQL, Redis, Celery workers, and Flower monitoring.

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    image: mydjango:${VERSION:-latest}
    container_name: django-web
    restart: unless-stopped
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully
    volumes:
      - static-files:/app/staticfiles
      - media-files:/app/media
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  migrations:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django-migrations
    command: python manage.py migrate --noinput
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django_db
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    restart: "no"

  celery-worker:
    build:
      context: .
      dockerfile: Dockerfile
    image: mydjango:${VERSION:-latest}
    container_name: django-celery-worker
    restart: unless-stopped
    command: celery -A config worker -l INFO --concurrency=4
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django_db
      - CELERY_BROKER_URL=redis://redis:6379/1
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
          cpus: "1.0"
          memory: 1G

  celery-beat:
    build:
      context: .
      dockerfile: Dockerfile
    image: mydjango:${VERSION:-latest}
    container_name: django-celery-beat
    restart: unless-stopped
    command: celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django_db
      - CELERY_BROKER_URL=redis://redis:6379/1
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend

  flower:
    image: mher/flower:2.0
    container_name: django-flower
    restart: unless-stopped
    command: celery --broker=redis://redis:6379/1 flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - frontend
      - backend
    environment:
      - FLOWER_BASIC_AUTH=${FLOWER_USER}:${FLOWER_PASSWORD}

  db:
    image: postgres:16-alpine
    container_name: django-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: django
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: django_db
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django -d django_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:7-alpine
    container_name: django-redis
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
  postgres-data:
  redis-data:
  static-files:
  media-files:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

---

## Example 3: Development with Hot Reload

Base + override pattern for development.

**docker-compose.yml** (base):

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: devdb
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  app-network:
```

**docker-compose.override.yml** (auto-loaded in development):

```yaml
services:
  app:
    build:
      target: development
    ports:
      - "3000:3000"
      - "9229:9229"  # Debugger
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev

  db:
    ports:
      - "5432:5432"
```

**docker-compose.prod.yml** (production overlay):

```yaml
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
      replicas: 2
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
```

**Usage:**

```bash
# Development (uses override automatically)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Example 4: Microservices with Service Discovery

```yaml
services:
  api-gateway:
    image: nginx:1.25-alpine
    container_name: api-gateway
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      user-service:
        condition: service_healthy
      order-service:
        condition: service_healthy
      product-service:
        condition: service_healthy
    networks:
      - frontend
      - backend

  user-service:
    build:
      context: ./services/user
    image: user-service:${VERSION:-latest}
    container_name: user-service
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://user:${DB_PASSWORD}@user-db:5432/users
    depends_on:
      user-db:
        condition: service_healthy
    networks:
      backend:
        aliases:
          - users
          - user-api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  order-service:
    build:
      context: ./services/order
    image: order-service:${VERSION:-latest}
    container_name: order-service
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://order:${DB_PASSWORD}@order-db:5432/orders
      - USER_SERVICE_URL=http://users:8000
      - PRODUCT_SERVICE_URL=http://products:8000
    depends_on:
      order-db:
        condition: service_healthy
      user-service:
        condition: service_healthy
      product-service:
        condition: service_healthy
    networks:
      backend:
        aliases:
          - orders
          - order-api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  product-service:
    build:
      context: ./services/product
    image: product-service:${VERSION:-latest}
    container_name: product-service
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://product:${DB_PASSWORD}@product-db:5432/products
    depends_on:
      product-db:
        condition: service_healthy
    networks:
      backend:
        aliases:
          - products
          - product-api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  user-db:
    image: postgres:16-alpine
    container_name: user-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: users
    volumes:
      - user-db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d users"]
      interval: 10s
      timeout: 5s
      retries: 5

  order-db:
    image: postgres:16-alpine
    container_name: order-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: order
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: orders
    volumes:
      - order-db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U order -d orders"]
      interval: 10s
      timeout: 5s
      retries: 5

  product-db:
    image: postgres:16-alpine
    container_name: product-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: product
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: products
    volumes:
      - product-db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U product -d products"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  user-db-data:
  order-db-data:
  product-db-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

---

## Example 5: Monitoring Stack

Prometheus, Grafana, and Node Exporter.

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.50.0
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/rules:/etc/prometheus/rules:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
      - '--web.enable-lifecycle'
    networks:
      - monitoring
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  grafana:
    image: grafana/grafana:10.4.0
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    depends_on:
      prometheus:
        condition: service_healthy
    networks:
      - monitoring
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  node-exporter:
    image: prom/node-exporter:v1.7.0
    container_name: node-exporter
    restart: unless-stopped
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:v0.27.0
    container_name: alertmanager
    restart: unless-stopped
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager-data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    networks:
      - monitoring
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:9093/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  prometheus-data:
  grafana-data:
  alertmanager-data:

networks:
  monitoring:
    driver: bridge
```

---

*Docker Compose Examples | faion-cicd-engineer*
