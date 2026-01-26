# Docker Checklists

Comprehensive checklists for Dockerfile quality, security, and production readiness.

---

## Dockerfile Quality Checklist

### Base Image

- [ ] Base image version is pinned (not `latest`)
- [ ] Using minimal base image (slim/alpine/distroless)
- [ ] Base image is from official/trusted source
- [ ] Base image updated recently (check for CVEs)

### Build Optimization

- [ ] .dockerignore is present and comprehensive
- [ ] Layer caching optimized (dependencies before code)
- [ ] RUN commands combined where appropriate
- [ ] Multi-stage build used (if applicable)
- [ ] No unnecessary files in final image
- [ ] Cache mounts used for package managers (`--mount=type=cache`)

### Instructions

- [ ] WORKDIR set before COPY/ADD
- [ ] COPY preferred over ADD (unless extracting archives)
- [ ] Exec form used for CMD/ENTRYPOINT
- [ ] HEALTHCHECK defined
- [ ] Labels present for metadata (maintainer, version)
- [ ] EXPOSE documented for ports

### User & Permissions

- [ ] Non-root user created and used
- [ ] Files copied with correct ownership (`--chown`)
- [ ] Minimal permissions on sensitive files

---

## Security Checklist

### Image Security

- [ ] No secrets embedded in image (use build secrets or runtime injection)
- [ ] No private keys in image
- [ ] No credentials in environment variables
- [ ] Image scanned for vulnerabilities (Trivy, Docker Scout)
- [ ] Signed images used where possible

### Runtime Security

- [ ] Running as non-root user
- [ ] Read-only filesystem (`--read-only`) where possible
- [ ] All capabilities dropped (`--cap-drop ALL`)
- [ ] Only necessary capabilities added (`--cap-add`)
- [ ] `no-new-privileges` security option set
- [ ] Resource limits defined (CPU, memory)

### Network Security

- [ ] Minimal ports exposed
- [ ] Internal-only services not exposed externally
- [ ] TLS used for external communications
- [ ] Network policies in place (if using orchestration)

### Secrets Management

- [ ] Docker Secrets used (not ENV for sensitive data)
- [ ] Secrets mounted as files, not environment variables
- [ ] External vault integration for production
- [ ] Secrets rotated regularly

### Vulnerability Management

- [ ] Regular image scanning in CI/CD
- [ ] Base images updated monthly (or more frequently)
- [ ] Dependency vulnerabilities patched
- [ ] CVE monitoring in place

---

## Production Readiness Checklist

### Image Quality

- [ ] Image tagged with semantic version + git SHA
- [ ] Image tested in staging environment
- [ ] Image size optimized (<500MB for most apps)
- [ ] No development tools in production image
- [ ] .dockerignore excludes test files, docs, etc.

### Health & Monitoring

- [ ] HEALTHCHECK configured with appropriate intervals
- [ ] Logging to stdout/stderr (not files)
- [ ] Structured logging (JSON format)
- [ ] Metrics endpoint exposed (if applicable)
- [ ] Graceful shutdown handled (SIGTERM)

### Configuration

- [ ] All configuration via environment variables
- [ ] Sensible defaults provided
- [ ] Environment variables documented
- [ ] Config validation at startup
- [ ] No hardcoded URLs/endpoints

### Resource Management

- [ ] Memory limits set (`--memory`)
- [ ] CPU limits set (`--cpus`)
- [ ] Storage limits considered
- [ ] Restart policy defined (`unless-stopped` or `always`)

### Deployment

- [ ] Rolling update strategy defined
- [ ] Rollback procedure documented
- [ ] Blue-green or canary deployment ready (if applicable)
- [ ] Database migration strategy defined
- [ ] Backup/restore procedures tested

---

## Docker Compose Checklist

### Configuration

- [ ] Version specified (3.9 or later)
- [ ] Services clearly named
- [ ] Build context and Dockerfile specified
- [ ] Networks explicitly defined
- [ ] Volumes explicitly defined

### Dependencies

- [ ] `depends_on` with health conditions used
- [ ] Service startup order correct
- [ ] Database migrations handled separately
- [ ] External dependencies documented

### Environment

- [ ] `.env` file for local development
- [ ] Production values NOT in docker-compose.yml
- [ ] Sensitive values in secrets or external config
- [ ] Override files for different environments

### Networking

- [ ] Custom networks defined (not default bridge)
- [ ] Service aliases configured if needed
- [ ] Ports exposed only where necessary
- [ ] Internal services use internal networks

### Volumes

- [ ] Named volumes for persistent data
- [ ] Bind mounts for development only
- [ ] Read-only mounts where applicable
- [ ] Volume backup strategy defined

---

## Multi-Stage Build Checklist

### Stage Organization

- [ ] Clear stage names (builder, runtime, etc.)
- [ ] Build tools only in builder stage
- [ ] Runtime dependencies in final stage only
- [ ] Minimal layers in final stage

### Optimization

- [ ] Build cache maximized
- [ ] Only necessary artifacts copied to final stage
- [ ] Virtual environment or node_modules optimized
- [ ] Static files handled appropriately

### Security

- [ ] No build secrets in final image
- [ ] No source code in final image (if compiled)
- [ ] Non-root user in final stage
- [ ] Minimal attack surface

---

## CI/CD Integration Checklist

### Build Pipeline

- [ ] Dockerfile linted (Hadolint)
- [ ] Image built with BuildKit
- [ ] Build cache utilized
- [ ] Multi-platform builds configured (if needed)

### Security Pipeline

- [ ] Image scanned before push
- [ ] Critical vulnerabilities block deployment
- [ ] SBOM generated (Software Bill of Materials)
- [ ] Signed images (if required)

### Registry

- [ ] Image pushed to private registry
- [ ] Multiple tags applied (version, SHA, latest)
- [ ] Old images cleaned up periodically
- [ ] Registry access controlled

### Deployment

- [ ] Image digest used (not just tag)
- [ ] Deployment validated with smoke tests
- [ ] Rollback automated on failure
- [ ] Monitoring alerts configured

---

## Quick Audit Commands

```bash
# Check image for issues
docker scout cves myapp:latest
trivy image myapp:latest
hadolint Dockerfile

# Analyze image size
dive myapp:latest
docker history myapp:latest

# Check running container security
docker inspect --format='{{.Config.User}}' container_name
docker inspect --format='{{.HostConfig.ReadonlyRootfs}}' container_name
docker inspect --format='{{.HostConfig.CapDrop}}' container_name

# Resource usage
docker stats container_name

# Health status
docker inspect --format='{{.State.Health.Status}}' container_name
```

---

## Checklist Summary by Priority

### Critical (Must Fix)

1. Running as non-root
2. No secrets in image
3. Base image pinned and scanned
4. Health checks configured
5. Resource limits set

### Important (Should Fix)

1. Multi-stage builds
2. .dockerignore present
3. Layer caching optimized
4. Read-only filesystem
5. Capabilities dropped

### Nice to Have

1. Image signing
2. SBOM generation
3. Distroless base images
4. Advanced BuildKit features
5. Automated vulnerability alerts
