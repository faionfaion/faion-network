# Docker Compose Checklists

**Production Readiness, Configuration, and Verification (2025-2026)**

---

## Compose File Checklist

### Modern Configuration

- [ ] No `version:` field (obsolete in 2025-2026)
- [ ] File named `compose.yaml` (not docker-compose.yml)
- [ ] Using `docker compose` CLI (not docker-compose)
- [ ] Syntax validated with `docker compose config`

### Services

- [ ] Health checks defined for ALL services
- [ ] `depends_on` with `condition: service_healthy`
- [ ] `restart: unless-stopped` or `always`
- [ ] Resource limits defined (memory, cpus, pids)
- [ ] Logging configured with rotation
- [ ] Environment via `.env` file (not hardcoded)

### Networking

- [ ] Custom networks defined (not default bridge)
- [ ] Backend network marked `internal: true`
- [ ] Database ports NOT exposed externally
- [ ] Only necessary ports mapped
- [ ] Frontend/backend/database tier separation

### Volumes

- [ ] Named volumes for persistent data
- [ ] Read-only mounts where possible (`:ro`)
- [ ] Bind mounts only for development
- [ ] tmpfs for temporary data

### Security

- [ ] Non-root user (`user: "1000:1000"`)
- [ ] Read-only filesystem (`read_only: true`)
- [ ] Capabilities dropped (`cap_drop: [ALL]`)
- [ ] No-new-privileges (`security_opt`)
- [ ] Secrets via Docker secrets or vault (not ENV)
- [ ] `.env` not committed to git
- [ ] `.env.example` provided

---

## Service Configuration Checklist

### Image

- [ ] Image pinned with version tag (not `latest`)
- [ ] Image from trusted registry
- [ ] Pull policy configured (if needed)

### Build

- [ ] Build target specified (dev/prod)
- [ ] Build args for version metadata
- [ ] `.dockerignore` present

### Environment

- [ ] Sensitive values via `env_file` or secrets
- [ ] Default values provided where appropriate
- [ ] No hardcoded credentials

### Health Check

- [ ] `test` command defined
- [ ] `interval` appropriate for service type
- [ ] `timeout` reasonable for endpoint
- [ ] `start_period` accounts for startup time
- [ ] `retries` set for tolerance

### Dependencies

- [ ] `depends_on` with condition specified
- [ ] Init containers complete before app starts
- [ ] Circular dependencies avoided

---

## Network Checklist

### Architecture

- [ ] Custom bridge networks created
- [ ] Internal network for backend services
- [ ] Database network isolated
- [ ] Service mesh for microservices (if needed)

### Configuration

- [ ] DNS names used (not IPs)
- [ ] Network aliases configured (if needed)
- [ ] IPv6 disabled if not needed

### Security

- [ ] Default bridge network not used
- [ ] Inter-container communication controlled
- [ ] Ingress traffic filtered
- [ ] No unnecessary port exposure

---

## Volume Checklist

### Configuration

- [ ] Named volumes for persistent data
- [ ] Volume drivers appropriate for environment
- [ ] Backup strategy defined
- [ ] Recovery tested

### Security

- [ ] Read-only mounts for configs (`:ro`)
- [ ] No host path mounts in production
- [ ] Sensitive directories protected
- [ ] tmpfs for sensitive temporary data

### Data Management

- [ ] Data retention policy defined
- [ ] Volume cleanup automated
- [ ] Orphaned volumes cleaned
- [ ] Storage quotas considered

---

## Production Deployment Checklist

### Pre-deployment

- [ ] Compose file validated (`docker compose config`)
- [ ] All images available in registry
- [ ] Environment variables configured
- [ ] Secrets deployed to host
- [ ] Networks pre-created (if external)
- [ ] Volumes pre-created (if external)

### Security

- [ ] All services run as non-root
- [ ] Resource limits enforced
- [ ] Secrets via Docker secrets or vault
- [ ] No privileged mode
- [ ] Capabilities minimized
- [ ] TLS for external connections

### Monitoring

- [ ] Health endpoints responding
- [ ] Metrics exposed (Prometheus format)
- [ ] Logs structured (JSON)
- [ ] Alerts configured
- [ ] Dashboards created

### Operations

- [ ] Backup procedures documented
- [ ] Rollback plan ready
- [ ] Scaling procedures documented
- [ ] On-call rotation defined

---

## Health Check Patterns Checklist

### HTTP Service

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  start_period: 40s
  retries: 3
```

- [ ] Endpoint responds with 2xx
- [ ] Endpoint checks critical dependencies
- [ ] Timeout less than interval
- [ ] Start period accounts for startup

### Database

```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
  interval: 10s
  timeout: 5s
  retries: 5
```

- [ ] Uses native health check command
- [ ] Checks specific database
- [ ] Uses correct user

### Redis

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

- [ ] Verifies Redis responds to ping
- [ ] Short interval for cache service

---

## Resource Limits Checklist

### Guidelines

| Service Type | CPU | Memory | PIDs |
|--------------|-----|--------|------|
| API (low traffic) | 0.5-1.0 | 256-512M | 50 |
| API (high traffic) | 1.0-2.0 | 512M-1G | 100 |
| Worker | 0.5-1.0 | 256-512M | 50 |
| Database | 1.0-4.0 | 1-4G | 200 |
| Redis | 0.25-0.5 | 64-256M | 50 |
| Nginx | 0.25-0.5 | 64-128M | 50 |

### Configuration

```yaml
deploy:
  resources:
    limits:
      cpus: "1.0"
      memory: 512M
      pids: 100
    reservations:
      cpus: "0.25"
      memory: 128M
```

- [ ] Limits set for all services
- [ ] Reservations ensure minimum resources
- [ ] PID limits prevent fork bombs
- [ ] Memory limits prevent OOM on host

---

## Development Override Checklist

### compose.override.yaml

- [ ] Build target: development
- [ ] Source code mounted as bind volume
- [ ] Debug ports exposed
- [ ] Hot-reload enabled
- [ ] Database ports exposed for local tools
- [ ] Mail server (mailhog) included
- [ ] DEBUG environment enabled

### Verification

- [ ] `docker compose config` shows merged config
- [ ] Development tools accessible
- [ ] Code changes reflected immediately
- [ ] Logs verbose enough for debugging

---

## Scaling Checklist

### Prerequisites

- [ ] `container_name` removed from scalable services
- [ ] Stateless application design
- [ ] Load balancer configured
- [ ] Session affinity (if needed)

### Configuration

- [ ] Replicas specified in deploy
- [ ] Update config for rolling updates
- [ ] Rollback config defined
- [ ] Health check gates deployment

### Verification

- [ ] `docker compose ps` shows all replicas
- [ ] Load balancer distributes traffic
- [ ] Rolling updates work correctly
- [ ] Rollback succeeds

---

## Multi-File Compose Checklist

### File Structure

```
compose.yaml           # Base (production-ready)
compose.override.yaml  # Development (auto-merged)
compose.prod.yaml      # Production overrides
compose.test.yaml      # Test configuration
.env                   # Environment variables
.env.example           # Template for .env
```

### Verification

- [ ] Base file is complete production config
- [ ] Override adds only dev-specific settings
- [ ] Prod file adjusts for production scale
- [ ] Test file includes test services
- [ ] `docker compose config -f` shows correct merge

---

## Migration Checklist (Legacy to Modern)

### Compose File

- [ ] Remove `version:` field
- [ ] Rename to `compose.yaml`
- [ ] Update to `docker compose` commands
- [ ] Add health checks to all services
- [ ] Add `depends_on` with conditions
- [ ] Add resource limits
- [ ] Configure logging with rotation
- [ ] Add security options

### Services

- [ ] Replace `links` with networks
- [ ] Replace `expose` with network isolation
- [ ] Add `restart` policy
- [ ] Add `user` for non-root

### Verification

- [ ] `docker compose config` validates
- [ ] All services start correctly
- [ ] Dependencies resolve properly
- [ ] Data persists across restarts

---

## Troubleshooting Checklist

### Service Won't Start

- [ ] Check logs: `docker compose logs service`
- [ ] Verify image exists
- [ ] Check port conflicts
- [ ] Verify volume permissions
- [ ] Check environment variables

### Health Check Failing

- [ ] Verify endpoint exists
- [ ] Check network connectivity
- [ ] Increase start_period
- [ ] Check container logs
- [ ] Test health command manually

### Network Issues

- [ ] Verify services on same network
- [ ] Use service name (not IP)
- [ ] Check DNS resolution
- [ ] Verify port is exposed in container

### Volume Issues

- [ ] Check volume exists: `docker volume ls`
- [ ] Verify mount path
- [ ] Check permissions (UID/GID)
- [ ] Verify read/write mode

---

## Quick Verification Commands

```bash
# Validate compose file
docker compose config --quiet

# Check service status
docker compose ps

# Check health status
docker compose ps --format json | jq '.[].Health'

# View resource usage
docker compose top
docker stats --no-stream

# Test network connectivity
docker compose exec app ping db
docker compose exec app nslookup db

# Check logs for errors
docker compose logs --tail 50 | grep -i error

# Verify volumes
docker volume ls
docker compose exec db ls -la /var/lib/postgresql/data

# Check environment
docker compose exec app env | sort
```

---

*Docker Compose Checklists | faion-infrastructure-engineer*
