# Docker Compose Checklist

## Pre-Deployment Verification

### Service Configuration

- [ ] No `version:` field (modern practice) or using 3.9+
- [ ] All services have explicit `container_name`
- [ ] `restart: unless-stopped` or `always` for production
- [ ] Resource limits defined (`cpus`, `memory`)
- [ ] Health checks configured for all critical services
- [ ] `depends_on` uses `condition: service_healthy`

### Security

- [ ] No hardcoded secrets in compose files
- [ ] Secrets in `.env` file (gitignored)
- [ ] `.env.example` committed as template
- [ ] Database ports NOT exposed in production
- [ ] Internal network for backend services
- [ ] Read-only mounts where possible (`:ro`)
- [ ] Non-root user in containers
- [ ] Images scanned for vulnerabilities (Trivy/Scout)

### Networking

- [ ] Frontend/backend network separation
- [ ] Backend network marked as `internal: true`
- [ ] Services communicate via service names
- [ ] Only necessary ports exposed to host

### Volumes

- [ ] Named volumes for persistent data
- [ ] Bind mounts only for development
- [ ] Database data on named volumes
- [ ] Log rotation configured
- [ ] Volume backups planned

### Logging

- [ ] Logging driver configured
- [ ] Log rotation enabled (`max-size`, `max-file`)
- [ ] Centralized logging for production (optional)

### Profiles

- [ ] Optional services use profiles
- [ ] Development tools in `dev` profile
- [ ] Workers/schedulers in separate profiles

## Environment-Specific

### Development

- [ ] `docker-compose.override.yml` for dev settings
- [ ] Debug ports exposed (9229 for Node.js)
- [ ] Source code mounted for live reload
- [ ] Database ports exposed for local tools
- [ ] `docker compose watch` configured (2025)

### Production

- [ ] Separate `docker-compose.prod.yml`
- [ ] Images pulled from registry (no build)
- [ ] `restart: always` policy
- [ ] Higher resource limits
- [ ] Replicas configured if needed
- [ ] SSL/TLS configured

### CI/CD

- [ ] Separate `docker-compose.test.yml`
- [ ] Test database isolated
- [ ] Cleanup after tests (`docker compose down -v`)

## Health Check Patterns

### HTTP Service

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### PostgreSQL

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Redis

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### MySQL/MariaDB

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### MongoDB

```yaml
healthcheck:
  test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### RabbitMQ

```yaml
healthcheck:
  test: ["CMD", "rabbitmq-diagnostics", "check_running"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Nginx

```yaml
healthcheck:
  test: ["CMD", "nginx", "-t"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Hardcoded secrets | Use `.env` files or Docker secrets |
| Missing health checks | Always define for critical services |
| Bind mounts in prod | Use named volumes |
| No resource limits | Set `cpus` and `memory` limits |
| Exposed DB ports in prod | Only expose in override files |
| Missing restart policy | Use `unless-stopped` or `always` |
| `depends_on` without condition | Use `condition: service_healthy` |
| No log rotation | Configure `max-size` and `max-file` |
| Single network | Separate frontend/backend |
| Building in production | Use pre-built images from registry |

## Verification Commands

```bash
# Validate compose file
docker compose config

# Check service status
docker compose ps

# View service health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

# Inspect network
docker network inspect $(docker compose ps -q | head -1 | xargs docker inspect --format='{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}')

# Check resource usage
docker stats --no-stream

# Verify volumes
docker volume ls
```
