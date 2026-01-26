# Docker Compose Examples

## Full-Stack Web Application

Production-ready setup with app, database, cache, reverse proxy, and worker.

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - VERSION=${VERSION:-latest}
    image: myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
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
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - frontend
      - backend
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
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
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
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

  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
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

  worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:${VERSION:-latest}
    container_name: myapp-worker
    restart: unless-stopped
    command: celery -A app worker --loglevel=info --concurrency=2
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
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
  static-files:
```

## Development Override

`docker-compose.override.yml` - automatically loaded in development.

```yaml
services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: npm run dev
    ports:
      - "8000:8000"
      - "9229:9229"  # Debug port

  db:
    ports:
      - "5432:5432"  # Expose for local tools

  redis:
    ports:
      - "6379:6379"  # Expose for local tools

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

## Production Override

`docker-compose.prod.yml` - use with `-f` flag.

```yaml
services:
  app:
    image: registry.example.com/myapp:${VERSION}
    build: null  # Don't build in production
    restart: always
    deploy:
      mode: replicated
      replicas: 2
      resources:
        limits:
          cpus: "2.0"
          memory: 1G

  db:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  nginx:
    restart: always
```

## Next.js + PostgreSQL

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: nextjs-app
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://app:${DB_PASSWORD}@db:5432/appdb
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=${NEXTAUTH_URL:-http://localhost:3000}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - default

  db:
    image: postgres:16-alpine
    container_name: nextjs-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

## Django + PostgreSQL + Redis + Celery

```yaml
services:
  web:
    build: .
    container_name: django-web
    restart: unless-stopped
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend

  celery:
    build: .
    container_name: django-celery
    restart: unless-stopped
    command: celery -A config worker -l INFO
    environment:
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
    profiles:
      - worker

  celery-beat:
    build: .
    container_name: django-celery-beat
    restart: unless-stopped
    command: celery -A config beat -l INFO
    environment:
      - DATABASE_URL=postgres://django:${DB_PASSWORD}@db:5432/django
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - celery
    networks:
      - backend
    profiles:
      - worker

  db:
    image: postgres:16-alpine
    container_name: django-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=django
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=django
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django -d django"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    container_name: django-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

networks:
  backend:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

## FastAPI + MongoDB + RabbitMQ

```yaml
services:
  api:
    build: .
    container_name: fastapi-api
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/fastapi
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    depends_on:
      mongo:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend

  mongo:
    image: mongo:7
    container_name: fastapi-mongo
    restart: unless-stopped
    volumes:
      - mongo-data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: fastapi-rabbitmq
    restart: unless-stopped
    ports:
      - "15672:15672"  # Management UI
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend

networks:
  backend:
    driver: bridge

volumes:
  mongo-data:
  rabbitmq-data:
```

## Monitoring Stack (Prometheus + Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    depends_on:
      - prometheus
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus-data:
  grafana-data:
```

## AI/ML Development with GPU

```yaml
services:
  jupyter:
    image: jupyter/tensorflow-notebook:latest
    container_name: ml-jupyter
    restart: unless-stopped
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_TOKEN=${JUPYTER_TOKEN:-}
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - ml

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    container_name: ml-mlflow
    restart: unless-stopped
    command: mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri postgresql://mlflow:${DB_PASSWORD}@db:5432/mlflow --default-artifact-root /mlflow/artifacts
    ports:
      - "5000:5000"
    volumes:
      - mlflow-artifacts:/mlflow/artifacts
    depends_on:
      db:
        condition: service_healthy
    networks:
      - ml

  db:
    image: postgres:16-alpine
    container_name: ml-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=mlflow
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=mlflow
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlflow -d mlflow"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - ml

networks:
  ml:
    driver: bridge

volumes:
  mlflow-artifacts:
  postgres-data:
```

## Watch Configuration (2025)

Enable live reload without restart.

```yaml
services:
  app:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
        - action: sync+restart
          path: ./config
          target: /app/config
```

Usage: `docker compose watch`
