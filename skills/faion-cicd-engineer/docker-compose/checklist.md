# Docker Compose Checklist

**Production readiness and best practices verification**

---

## Pre-Deployment Checklist

### Image Configuration

- [ ] Images tagged with specific version (not `latest`)
- [ ] Using official or verified publisher images
- [ ] Multi-stage builds for smaller images
- [ ] Images scanned for vulnerabilities (Trivy, Docker Scout)

### Service Configuration

- [ ] `restart` policy defined (`unless-stopped` or `on-failure`)
- [ ] `container_name` set for identification
- [ ] Resource limits defined (CPU, memory)
- [ ] Resource reservations set for critical services

### Health Checks

- [ ] Health check defined for each service
- [ ] Appropriate `interval`, `timeout`, `retries` values
- [ ] `start_period` set for services with slow startup
- [ ] Application-specific health endpoints (not just port check)

### Dependencies

- [ ] `depends_on` with `service_healthy` for databases
- [ ] Startup order verified
- [ ] No circular dependencies
- [ ] Migration services use `service_completed_successfully`

### Networking

- [ ] Networks explicitly defined
- [ ] Services on appropriate networks only
- [ ] No unnecessary port exposures
- [ ] Internal services not exposed to host

### Volumes

- [ ] Named volumes for persistent data
- [ ] Bind mounts read-only where possible (`:ro`)
- [ ] Database volumes defined and named
- [ ] No sensitive data in bind mounts

### Security

- [ ] No secrets in environment variables
- [ ] Using Docker secrets or external vault
- [ ] `read_only: true` where possible
- [ ] Capabilities dropped (`cap_drop: ALL`)
- [ ] Only required capabilities added
- [ ] `no-new-privileges` security option set
- [ ] Non-root user specified in Dockerfile

### Environment

- [ ] Environment variables documented
- [ ] Using `.env` file (not in version control)
- [ ] Separate configs for dev/staging/prod
- [ ] No hardcoded credentials

### Logging

- [ ] Logging to stdout/stderr
- [ ] Log driver configured if needed
- [ ] Log rotation configured
- [ ] Structured logging (JSON) enabled

### Operational

- [ ] Graceful shutdown handled (SIGTERM)
- [ ] Stop timeout configured if needed
- [ ] Backup strategy for volumes
- [ ] Monitoring endpoints exposed

---

## Environment-Specific Checklists

### Development

- [ ] Hot reload enabled (bind mounts)
- [ ] Debug ports exposed
- [ ] Override file configured
- [ ] Development tools included

### Staging

- [ ] Mirrors production configuration
- [ ] Test data seeding configured
- [ ] CI/CD integration verified
- [ ] Performance baseline established

### Production

- [ ] All security items checked
- [ ] Resource limits verified
- [ ] Health checks tested
- [ ] Rollback procedure documented
- [ ] Disaster recovery plan in place

---

## Health Check Verification

### Database Services

```bash
# PostgreSQL
docker compose exec db pg_isready -U postgres

# MySQL
docker compose exec db mysqladmin ping -h localhost

# Redis
docker compose exec redis redis-cli ping

# MongoDB
docker compose exec mongo mongosh --eval "db.adminCommand('ping')"
```

### Application Services

```bash
# Check container health status
docker compose ps

# Check specific service health
docker inspect --format='{{.State.Health.Status}}' container_name

# View health check logs
docker inspect --format='{{json .State.Health}}' container_name | jq
```

---

## Pre-Production Validation

```bash
# Validate compose file syntax
docker compose config

# Check for issues
docker compose config --quiet

# Dry run (Compose v2)
docker compose up --dry-run

# Test build process
docker compose build --no-cache

# Verify network connectivity
docker compose up -d
docker compose exec app ping db

# Test graceful shutdown
docker compose down --timeout 30
```

---

## Security Audit Commands

```bash
# Scan images for vulnerabilities
docker scout cves myimage:latest

# Or with Trivy
trivy image myimage:latest

# Check running containers
docker compose ps --format json | jq

# Inspect security settings
docker inspect container_name | jq '.[0].HostConfig.SecurityOpt'

# Check capabilities
docker inspect container_name | jq '.[0].HostConfig.CapAdd, .[0].HostConfig.CapDrop'
```

---

## Quick Reference

### Restart Policies

| Scenario | Policy |
|----------|--------|
| Critical services | `unless-stopped` |
| Worker processes | `on-failure:5` |
| One-time tasks | `no` |
| Always running | `always` |

### Health Check Timing

| Service Type | Interval | Timeout | Retries | Start Period |
|--------------|----------|---------|---------|--------------|
| Web app | 30s | 10s | 3 | 30s |
| Database | 10s | 5s | 5 | 60s |
| Cache | 10s | 5s | 3 | 10s |
| Queue | 15s | 10s | 3 | 30s |

### Resource Limits (Starting Points)

| Service | CPU Limit | Memory Limit |
|---------|-----------|--------------|
| Node.js app | 0.5 | 512M |
| Python app | 0.5 | 512M |
| PostgreSQL | 1.0 | 1G |
| Redis | 0.25 | 256M |
| Nginx | 0.25 | 128M |

---

*Docker Compose Checklist | faion-cicd-engineer*
