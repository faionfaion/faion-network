# Docker Checklists

**Production Readiness, Security Hardening, and Verification (2025-2026)**

---

## Dockerfile Checklist

### Base Image

- [ ] Version pinned with digest (e.g., `python:3.12.1-slim@sha256:...`)
- [ ] Slim, Alpine, or Distroless variant for production
- [ ] Official image from trusted source (Docker Hub Official, Chainguard)
- [ ] Image regularly updated (check for CVEs weekly)
- [ ] No `latest` tag in production

### Build Optimization

- [ ] Multi-stage build implemented
- [ ] .dockerignore present and complete
- [ ] Layer order optimized (deps before code)
- [ ] RUN commands combined with &&
- [ ] BuildKit cache mounts used (`--mount=type=cache`)
- [ ] COPY preferred over ADD
- [ ] `# syntax=docker/dockerfile:1` at top

### Security (2025-2026)

- [ ] Non-root user created and used (UID 1000+)
- [ ] No secrets in Dockerfile or ENV
- [ ] No sensitive data in build args
- [ ] Minimal packages installed
- [ ] `rm -rf /var/lib/apt/lists/*` after apt-get
- [ ] No curl/wget piped to shell
- [ ] Package verification enabled (checksums)
- [ ] BuildKit secrets used for build-time credentials

### Runtime

- [ ] HEALTHCHECK defined
- [ ] EXPOSE documented
- [ ] Exec form for CMD/ENTRYPOINT (JSON array)
- [ ] Labels for metadata (version, maintainer, git-sha)
- [ ] WORKDIR set (not relying on default)

---

## Docker Compose Checklist

### Configuration

- [ ] No `version:` field (modern compose)
- [ ] File named `compose.yaml`
- [ ] Environment variables via .env file
- [ ] .env not committed to git
- [ ] .env.example provided
- [ ] Sensitive values use Docker secrets

### Services

- [ ] Health checks for ALL services
- [ ] `depends_on` with `condition: service_healthy`
- [ ] `restart: unless-stopped` (or `always`)
- [ ] Resource limits (memory, cpus) defined
- [ ] Logging configured with rotation
- [ ] Container names defined

### Networking

- [ ] Custom networks defined (not default bridge)
- [ ] Backend network marked `internal: true`
- [ ] Database ports NOT exposed in production
- [ ] Only necessary ports mapped
- [ ] Frontend/backend/database tier separation

### Volumes

- [ ] Named volumes for persistent data
- [ ] Read-only mounts where possible (`:ro`)
- [ ] Bind mounts only for development
- [ ] tmpfs for temporary data

---

## Production Deployment Checklist

### Pre-deployment

- [ ] Image tagged with semantic version + git SHA
- [ ] Image pushed to private registry
- [ ] Vulnerability scan passed (no CRITICAL)
- [ ] No HIGH CVEs (or approved exceptions)
- [ ] Image signed (Docker Content Trust or Cosign)
- [ ] SBOM generated and stored

### Runtime Configuration

- [ ] Resource limits enforced
- [ ] Read-only root filesystem enabled
- [ ] tmpfs for /tmp
- [ ] Health checks responding
- [ ] Logging to external system
- [ ] Metrics endpoint exposed

### Security

- [ ] Container runs as non-root (UID 1000+)
- [ ] Secrets via Docker secrets or vault
- [ ] No privileged mode
- [ ] Capabilities dropped (`--cap-drop ALL`)
- [ ] Seccomp profile applied
- [ ] AppArmor/SELinux profile applied
- [ ] `no-new-privileges` set

### Networking

- [ ] Internal network for backend services
- [ ] TLS for all external connections
- [ ] No database ports exposed externally
- [ ] Rate limiting on ingress
- [ ] Network policies defined

### Monitoring

- [ ] Health endpoint responding
- [ ] Metrics exposed (Prometheus format)
- [ ] Logs structured (JSON)
- [ ] Alerts configured
- [ ] Dashboards created

---

## Security Hardening Checklist (2025-2026)

### Image Security

- [ ] Base image from official/trusted source
- [ ] Image scanned with Trivy/Scout
- [ ] No CRITICAL vulnerabilities
- [ ] Regular base image updates (weekly)
- [ ] Content Trust or Cosign enabled
- [ ] SBOM generated and verified
- [ ] Distroless or Chainguard for high-security

### Container Security

- [ ] Non-root user (UID 1000+)
- [ ] Read-only filesystem
- [ ] No privileged mode
- [ ] Capabilities minimized (`--cap-drop ALL`)
- [ ] seccomp profile (default or custom)
- [ ] AppArmor profile applied
- [ ] `--security-opt=no-new-privileges:true`
- [ ] PID limits set
- [ ] Memory limits set

### Secret Management

- [ ] No secrets in Dockerfile
- [ ] No secrets in environment variables (in images)
- [ ] Docker secrets or external vault used
- [ ] Secrets rotated regularly
- [ ] Build-time secrets via `--mount=type=secret`
- [ ] Runtime secrets via volumes/env at deploy time

### Network Security

- [ ] Minimal port exposure
- [ ] Internal networks for backends
- [ ] TLS for all external traffic
- [ ] Network policies defined
- [ ] Container-to-container encryption (if needed)
- [ ] DNS rebinding protection

### Host Security

- [ ] Docker daemon socket protected
- [ ] No mounting of /var/run/docker.sock (except where required)
- [ ] User namespace remapping enabled
- [ ] Regular host and Docker updates
- [ ] Audit logging enabled

---

## Networking Checklist

### Network Architecture

- [ ] Custom bridge networks created
- [ ] Internal network for backend services
- [ ] Database network isolated
- [ ] Service mesh for microservices (if needed)

### Network Configuration

- [ ] DNS names used (not IPs)
- [ ] Container names match service names
- [ ] Network aliases configured
- [ ] IPv6 disabled if not needed

### Network Security

- [ ] Default bridge network not used
- [ ] Inter-container communication controlled
- [ ] Ingress traffic filtered
- [ ] Egress traffic limited (if possible)
- [ ] Network encryption for sensitive data

---

## Storage Checklist

### Volume Configuration

- [ ] Named volumes for persistent data
- [ ] Volume drivers appropriate for environment
- [ ] Backup strategy defined
- [ ] Recovery tested

### Mount Security

- [ ] Read-only mounts for configs (`:ro`)
- [ ] No host path mounts in production
- [ ] Sensitive directories protected
- [ ] tmpfs for sensitive temporary data

### Data Management

- [ ] Data retention policy defined
- [ ] Volume cleanup automated
- [ ] Orphaned volumes cleaned
- [ ] Storage quotas configured

---

## CI/CD Pipeline Checklist

### Build Stage

- [ ] Dockerfile linted (Hadolint)
- [ ] Build uses `--no-cache` for releases
- [ ] Multi-platform builds configured (amd64, arm64)
- [ ] Build args for version metadata
- [ ] BuildKit caching enabled

### Test Stage

- [ ] Unit tests pass in container
- [ ] Integration tests with compose
- [ ] Security scan (Trivy/Scout)
- [ ] Image size checked (threshold set)
- [ ] Healthcheck verified

### Scan Stage

- [ ] CVE scan completed
- [ ] SBOM generated
- [ ] License compliance checked
- [ ] Secret scanning performed
- [ ] Fail on CRITICAL/HIGH CVEs

### Push Stage

- [ ] Tagged with version and SHA
- [ ] Pushed to private registry
- [ ] Image signed with Cosign
- [ ] Old images cleaned up
- [ ] Retention policy applied

### Deploy Stage

- [ ] Health checks verified
- [ ] Rollback plan ready
- [ ] Monitoring alerts configured
- [ ] Post-deploy verification
- [ ] Canary deployment (if applicable)

---

## Image Size Optimization Checklist

- [ ] Multi-stage build used
- [ ] Alpine, slim, or distroless base
- [ ] Unnecessary packages removed
- [ ] Cache cleared after installs
- [ ] .dockerignore complete
- [ ] Build artifacts excluded
- [ ] Single layer for static assets
- [ ] Dive analysis reviewed
- [ ] Target size: <200MB for most apps

---

## Container Runtime Security Checklist (2025-2026)

### Seccomp

- [ ] Default seccomp profile enabled
- [ ] Custom profile for restricted workloads
- [ ] Syscalls minimized for each container
- [ ] Profile audited and tested

### AppArmor/SELinux

- [ ] AppArmor profile applied (Linux)
- [ ] SELinux context set (RHEL/CentOS)
- [ ] Mandatory access controls enforced
- [ ] Profile tested and validated

### Capabilities

- [ ] `--cap-drop ALL` applied
- [ ] Only needed capabilities added
- [ ] NET_BIND_SERVICE only if binding <1024
- [ ] No CAP_SYS_ADMIN
- [ ] No CAP_NET_RAW unless required

### Resource Limits

- [ ] Memory limit set (--memory)
- [ ] CPU limit set (--cpus)
- [ ] PID limit set (--pids-limit)
- [ ] Ulimits configured (--ulimit)
- [ ] Storage quota enforced

---

## Debugging Checklist

### Container Issues

- [ ] Check logs: `docker logs -f container`
- [ ] Check health: `docker inspect --format='{{.State.Health}}' container`
- [ ] Check resources: `docker stats container`
- [ ] Check processes: `docker top container`
- [ ] Exec into container: `docker exec -it container sh`

### Network Issues

- [ ] Check DNS: `docker exec container nslookup service`
- [ ] Check connectivity: `docker exec container ping service`
- [ ] Inspect network: `docker network inspect networkname`
- [ ] Check port bindings: `docker port container`
- [ ] Check iptables rules

### Build Issues

- [ ] Build with `--progress=plain`
- [ ] Check build context size
- [ ] Verify .dockerignore
- [ ] Test intermediate stages
- [ ] Check for layer caching issues

### Volume Issues

- [ ] Check volume exists: `docker volume ls`
- [ ] Inspect volume: `docker volume inspect volumename`
- [ ] Check permissions inside container
- [ ] Verify mount paths

---

## Quick Verification Commands

```bash
# Check image vulnerabilities
docker scout cves myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Lint Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile

# Analyze layers
dive myapp:latest

# Check running as non-root
docker run --rm myapp:latest id
docker run --rm myapp:latest whoami

# Verify health check
docker inspect --format='{{json .Config.Healthcheck}}' myapp:latest

# Check image size
docker images myapp:latest --format "{{.Size}}"

# Check security options
docker inspect --format='{{json .HostConfig.SecurityOpt}}' container

# Check capabilities
docker inspect --format='{{json .HostConfig.CapDrop}}' container
docker inspect --format='{{json .HostConfig.CapAdd}}' container

# Check read-only
docker inspect --format='{{.HostConfig.ReadonlyRootfs}}' container

# Verify no secrets in image
docker history --no-trunc myapp:latest | grep -i secret
docker history --no-trunc myapp:latest | grep -i password

# Check resource limits
docker inspect --format='{{.HostConfig.Memory}}' container
docker inspect --format='{{.HostConfig.NanoCpus}}' container

# Verify seccomp profile
docker inspect --format='{{.HostConfig.SecurityOpt}}' container
```

---

## Compliance Mapping

| Standard | Key Requirements |
|----------|------------------|
| **CIS Docker Benchmark** | Non-root, capabilities, seccomp, AppArmor |
| **NIST 800-190** | Image scanning, runtime security, network segmentation |
| **PCI-DSS** | Network segmentation, encryption, access control |
| **SOC 2** | Access control, logging, monitoring, change management |
| **HIPAA** | Encryption, audit logs, access control, data integrity |
| **GDPR** | Data protection, encryption, audit trails |

---

## DoS Protection Checklist

- [ ] Memory limits set
- [ ] CPU limits set
- [ ] PID limits configured
- [ ] Restart policy with backoff
- [ ] Rate limiting on ingress
- [ ] Connection limits configured
- [ ] File descriptor limits set

---

## Supply Chain Security Checklist (2025-2026)

- [ ] Base images from trusted registries only
- [ ] SBOM generated for all images
- [ ] Image signatures verified (Cosign)
- [ ] Vulnerability scanning in CI/CD
- [ ] Dependency scanning enabled
- [ ] License compliance checked
- [ ] Provenance attestation (SLSA)

---

*Docker Checklists | faion-infrastructure-engineer*
