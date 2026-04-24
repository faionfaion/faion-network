# Docker Compose Patterns Checklist

## Pre-Setup

- [ ] Docker Engine installed: `docker --version`
- [ ] Docker Compose V2 available: `docker compose version`
- [ ] Current user in docker group: `groups | grep docker`
- [ ] Docker daemon running: `systemctl status docker`
- [ ] Sufficient disk space for volumes: `df -h /var/lib/docker`

## Compose File Structure

### Services

- [ ] Each service has an explicit `image` with version tag (not `latest`)
- [ ] Each service has `container_name` for predictable naming
- [ ] Each service has `restart: unless-stopped`
- [ ] Ports bound to `127.0.0.1` (not `0.0.0.0`) for non-public services
- [ ] Environment variables use `env_file` for secrets (not inline `environment`)
- [ ] Working `command` override if needed (e.g., custom PostgreSQL parameters)

### Health Checks

- [ ] PostgreSQL: `pg_isready` health check configured
- [ ] Redis: `redis-cli ping` health check configured
- [ ] RabbitMQ: `rabbitmq-diagnostics ping` health check configured
- [ ] Health check has reasonable `start_period` for slow-starting services
- [ ] `depends_on` uses `condition: service_healthy` where appropriate

### Volumes

- [ ] Named volumes for persistent data (databases, message broker data)
- [ ] Bind mounts for configuration files (with `:ro` if read-only)
- [ ] No bind mounts to host paths that don't exist
- [ ] Volume names are descriptive and scoped to project

### Networking

- [ ] Default bridge network is sufficient (or custom networks defined)
- [ ] Internal services not exposed to host unnecessarily
- [ ] No `network_mode: host` unless specifically needed

### Resource Limits

- [ ] Memory limits set via `deploy.resources.limits.memory`
- [ ] CPU limits set if needed via `deploy.resources.limits.cpus`
- [ ] Limits are reasonable for the server's total resources
- [ ] Sum of all container limits does not exceed server capacity

### Logging

- [ ] Log rotation configured per-service or globally in daemon.json
- [ ] `max-size` set to prevent disk fill (e.g., `10m`)
- [ ] `max-file` set to limit log file count (e.g., `3`)

## Security

- [ ] No secrets hardcoded in docker-compose.yml
- [ ] `.env` file has proper permissions (chmod 600)
- [ ] `.env` file is in `.gitignore`
- [ ] Docker socket not mounted into any container (unless explicitly needed)
- [ ] Containers run as non-root where possible
- [ ] Images from trusted sources only (official, verified)
- [ ] No `privileged: true` unless required

## Production Readiness

### Data Persistence

- [ ] All databases use named volumes (data survives `docker compose down`)
- [ ] Tested: `docker compose down` then `docker compose up -d` preserves data
- [ ] Backup strategy for volumes documented

### Startup/Shutdown

- [ ] Services start in correct order (depends_on with health checks)
- [ ] `docker compose up -d` is idempotent (safe to run multiple times)
- [ ] Graceful shutdown works: `docker compose stop` (sends SIGTERM)

### Updates

- [ ] Image update process documented: pull, recreate, verify
- [ ] Data migration process for major version upgrades documented
- [ ] Tested rollback: can revert to previous image version

## Verification

- [ ] All services are running: `docker compose ps`
- [ ] All health checks pass: `docker compose ps` shows "healthy"
- [ ] Services can communicate: `docker compose exec service1 ping service2`
- [ ] Application can connect to services: test from host on 127.0.0.1
- [ ] Logs are being captured: `docker compose logs --tail 5 service-name`
- [ ] Resource usage is within limits: `docker stats`

## Maintenance

- [ ] Set up log rotation (daemon.json or per-service)
- [ ] Schedule docker system prune for cleanup
- [ ] Monitor disk usage of `/var/lib/docker`
- [ ] Document the complete `docker compose up` startup procedure
- [ ] Create backup scripts for named volumes
