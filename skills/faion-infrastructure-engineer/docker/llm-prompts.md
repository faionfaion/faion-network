# Docker LLM Prompts

**AI Prompts for Docker Infrastructure Tasks (2025-2026)**

---

## Dockerfile Generation

### Create Production Dockerfile

```
Create a production-ready Dockerfile for a [LANGUAGE/FRAMEWORK] application with:

Context:
- Application type: [web API / CLI / worker / etc.]
- Framework: [FastAPI/Django/Express/Next.js/etc.]
- Dependencies: [list key dependencies]
- Port: [application port]
- Health endpoint: [/health or similar]

Requirements:
1. Multi-stage build (builder + production)
2. Non-root user (uid 1000)
3. Layer caching optimization
4. HEALTHCHECK instruction
5. Security best practices (2025-2026):
   - Pinned base image version with digest
   - Minimal base (slim/distroless)
   - No secrets in image
   - Read-only filesystem support
   - BuildKit syntax header
6. Labels for metadata (maintainer, version, git-sha)

Output: Complete Dockerfile with comments explaining each section.
```

### Create Distroless/Chainguard Dockerfile

```
Create a maximum-security Dockerfile using distroless or Chainguard base for:

Application: [LANGUAGE/TYPE]
Binary type: [static/dynamic linked]
Needs: [list any runtime requirements]

Requirements:
1. Build stage with full toolchain
2. Production stage with distroless/chainguard
3. No shell in final image
4. nonroot user
5. Minimal attack surface

Provide:
- Complete Dockerfile
- Expected image size
- Security benefits explained
```

### Optimize Existing Dockerfile

```
Optimize this Dockerfile for production:

[PASTE EXISTING DOCKERFILE]

Analyze and improve:
1. Image size reduction (target: <200MB)
2. Build time optimization (layer caching)
3. Security hardening (2025-2026 standards)
4. Best practices alignment

Provide:
- Optimized Dockerfile
- Size/security improvements summary
- Explanation of changes
- Before/after comparison
```

### Debug Dockerfile Build

```
Debug this Dockerfile build failure:

Dockerfile:
[PASTE DOCKERFILE]

Error:
[PASTE ERROR MESSAGE]

Context:
- Base image: [image name]
- Build command: [docker build command]
- Platform: [linux/amd64 or linux/arm64]

Analyze the error and provide:
1. Root cause
2. Fix
3. Prevention tips
```

---

## Docker Compose Generation

### Create Full Stack Compose

```
Create a Docker Compose configuration for:

Application Stack:
- Application: [language/framework] on port [PORT]
- Database: [PostgreSQL/MySQL/MongoDB]
- Cache: [Redis/Memcached] (if needed)
- Reverse proxy: [nginx/traefik] (if needed)

Requirements:
1. Modern compose format (no version field)
2. Health checks with depends_on conditions
3. Named volumes for persistence
4. Network isolation (frontend/backend)
5. Resource limits
6. Environment via .env file
7. Logging with rotation
8. Security hardening:
   - Non-root users
   - Read-only where possible
   - cap_drop ALL
   - no-new-privileges

Include:
- compose.yaml (production base)
- compose.override.yaml (development)
- .env.example
- .dockerignore
```

### Create Microservices Compose

```
Create a Docker Compose for microservices architecture:

Services:
[LIST SERVICES AND THEIR RELATIONSHIPS]

Requirements:
1. Network segmentation per service
2. Internal networks for databases
3. API gateway for external access
4. Health checks for all services
5. Service discovery via DNS
6. Centralized logging

Provide:
- Complete compose.yaml
- Network diagram (text)
- Service communication patterns
```

### Migrate docker-compose.yml to Modern Format

```
Migrate this legacy docker-compose.yml to modern 2025-2026 format:

[PASTE OLD DOCKER-COMPOSE.YML]

Changes needed:
1. Remove version field
2. Rename to compose.yaml
3. Add health checks
4. Add depends_on with conditions
5. Add resource limits
6. Configure logging
7. Add security options
8. Use modern command format (docker compose)

Provide:
- Updated compose.yaml
- List of breaking changes
- Migration commands
```

---

## Security Analysis

### Security Audit Dockerfile

```
Perform a security audit on this Dockerfile:

[PASTE DOCKERFILE]

Check for (2025-2026 standards):
1. Root user usage
2. Hardcoded secrets
3. Unpinned versions (no digest)
4. Unnecessary packages
5. Missing health checks
6. Excessive capabilities
7. Build-time secrets exposure
8. Missing seccomp/AppArmor considerations
9. Shell in production images (distroless recommended)

Provide:
- Risk assessment (Critical/High/Medium/Low)
- Specific vulnerabilities found
- Remediation steps
- Hardened Dockerfile
```

### Analyze Container Security

```
Analyze security posture of this container deployment:

compose.yaml:
[PASTE COMPOSE FILE]

Check:
1. Privileged mode usage
2. Capability settings
3. User namespace
4. Network exposure
5. Volume permissions
6. Secret management
7. Resource limits (DoS protection)
8. Seccomp/AppArmor profiles

Provide:
- Security score (1-10)
- Critical issues
- Recommendations
- Hardened compose.yaml
```

### Create Security Baseline

```
Create a security baseline configuration for:

Environment: [development/staging/production]
Compliance: [CIS/NIST/PCI-DSS/SOC2/HIPAA] (if applicable)

Include:
1. Docker daemon configuration
2. Container runtime settings
3. Network policies
4. Resource limits
5. Logging requirements
6. Image scanning policies
7. Seccomp profile
8. AppArmor profile

Output:
- daemon.json configuration
- Compose security settings
- Seccomp profile JSON
- Compliance checklist
```

---

## Networking Prompts

### Design Network Architecture

```
Design Docker network architecture for:

Application: [DESCRIPTION]
Components:
- [LIST SERVICES]

Requirements:
- External access: [which services]
- Internal only: [which services]
- Database isolation: [yes/no]
- Compliance: [requirements if any]

Provide:
1. Network diagram (text-based)
2. Compose network configuration
3. Security considerations
4. Traffic flow explanation
```

### Debug Container Networking

```
Debug container networking issue:

Setup:
[DESCRIBE CONTAINER SETUP]

Problem:
[DESCRIBE THE ISSUE - e.g., "container A cannot reach container B"]

compose.yaml:
[PASTE COMPOSE FILE]

Error messages:
[PASTE RELEVANT ERRORS]

Provide:
1. Diagnostic commands to run
2. Likely root cause
3. Solution
4. Prevention tips
```

### Configure Network Segmentation

```
Configure network segmentation for:

Architecture:
- Frontend tier: [services]
- Application tier: [services]
- Database tier: [services]
- External integrations: [services]

Requirements:
- Zero trust between tiers
- Minimal port exposure
- Encrypted communication

Provide:
1. Network definitions
2. Service assignments
3. Firewall rules (iptables or network policies)
4. TLS configuration
```

---

## Storage Prompts

### Design Volume Strategy

```
Design volume strategy for:

Application: [DESCRIPTION]
Data types:
- [Persistent data - e.g., database]
- [Temporary data - e.g., cache]
- [Config data - e.g., settings]
- [Secrets - e.g., certificates]

Requirements:
- Backup frequency: [daily/weekly/etc.]
- Retention: [period]
- Encryption: [yes/no]

Provide:
1. Volume configuration
2. Mount strategy (named/bind/tmpfs)
3. Backup script
4. Recovery procedure
```

### Debug Volume Permissions

```
Debug volume permission issue:

Problem:
[DESCRIBE - e.g., "container cannot write to mounted volume"]

Container user: [UID:GID]
Host volume path: [PATH]
Host permissions: [ls -la output]

Provide:
1. Root cause
2. Fix options (Dockerfile vs runtime)
3. Best practice recommendation
```

---

## Optimization Prompts

### Reduce Image Size

```
Help reduce this Docker image size:

Current Dockerfile:
[PASTE DOCKERFILE]

Current size: [SIZE]
Target size: [TARGET SIZE or "as small as possible"]

Techniques to consider:
1. Multi-stage builds
2. Alpine/slim/distroless base
3. Layer optimization
4. Dependency pruning
5. .dockerignore improvements

Provide:
- Optimized Dockerfile
- Expected size reduction
- Trade-offs (if any)
```

### Improve Build Speed

```
Optimize Docker build speed:

Dockerfile:
[PASTE DOCKERFILE]

Current build time: [TIME]
CI/CD context: [GitHub Actions / GitLab CI / etc.]

Optimize for:
1. Layer caching
2. BuildKit features
3. Dependency caching
4. Parallel builds
5. Cache mounts

Provide:
- Optimized Dockerfile
- CI/CD cache configuration
- Expected improvement
```

### Optimize for Multi-Platform

```
Optimize Dockerfile for multi-platform builds:

Target platforms: [linux/amd64, linux/arm64, etc.]

Current Dockerfile:
[PASTE DOCKERFILE]

Requirements:
- Same functionality on all platforms
- Minimal platform-specific code
- Efficient cross-compilation

Provide:
- Multi-platform Dockerfile
- Build command
- Platform-specific considerations
```

---

## Troubleshooting Prompts

### Debug Container Health Check

```
Debug failing health check:

Container: [NAME]
Health check status: [unhealthy]

Dockerfile HEALTHCHECK:
[PASTE HEALTHCHECK]

Logs:
[PASTE RELEVANT LOGS]

Provide:
1. Diagnostic steps
2. Root cause analysis
3. Fixed HEALTHCHECK
4. Verification commands
```

### Debug Container Crash Loop

```
Debug container crash loop:

Container: [NAME]
Exit code: [CODE]

Docker logs:
[PASTE LOGS]

Dockerfile:
[PASTE DOCKERFILE]

Compose configuration:
[PASTE RELEVANT CONFIG]

Provide:
1. Root cause analysis
2. Solution
3. Prevention tips
```

### Debug Resource Issues

```
Debug container resource issues:

Symptoms:
[DESCRIBE - OOM killed, CPU throttling, etc.]

Current limits:
[PASTE RESOURCE CONFIG]

Container stats:
[docker stats output]

Application type: [DESCRIPTION]

Provide:
1. Analysis of resource usage
2. Recommended limits
3. Application optimization tips
```

---

## CI/CD Integration

### Create CI/CD Docker Pipeline

```
Create Docker CI/CD pipeline for:

Platform: [GitHub Actions / GitLab CI / etc.]
Registry: [Docker Hub / ECR / GCR / GHCR]

Pipeline stages:
1. Lint Dockerfile (Hadolint)
2. Build image
3. Security scan (Trivy/Scout)
4. SBOM generation
5. Test
6. Push to registry
7. Sign image (Cosign)
8. Deploy [optional]

Requirements:
- Multi-platform builds (amd64, arm64)
- Semantic versioning tags
- Cache optimization
- Fail on HIGH/CRITICAL CVEs

Provide:
- Complete pipeline file
- Explanation of each stage
```

### Integrate Vulnerability Scanning

```
Integrate vulnerability scanning into CI/CD:

CI Platform: [PLATFORM]
Scanner: [Trivy/Scout/Snyk]

Requirements:
- Scan on every PR
- Fail build on CRITICAL
- Generate reports
- Track over time

Provide:
- Pipeline configuration
- Policy configuration
- Reporting setup
```

---

## Production Operations

### Create Production Deployment

```
Create production deployment configuration:

Application: [DESCRIPTION]
Scale: [instances/replicas]
Infrastructure: [docker-compose/swarm/kubernetes]

Requirements:
- Zero-downtime deployment
- Health-based routing
- Resource limits
- Logging and monitoring
- Backup strategy
- Rollback capability

Provide:
- Complete deployment configuration
- Deployment script
- Rollback script
- Monitoring setup
```

### Design Disaster Recovery

```
Design Docker disaster recovery plan:

Infrastructure:
[DESCRIBE CURRENT SETUP]

Critical services: [LIST]
RPO: [Recovery Point Objective]
RTO: [Recovery Time Objective]

Provide:
1. Backup strategy
2. Recovery procedures
3. Testing plan
4. Automation scripts
```

---

## Quick Task Prompts

### Generate .dockerignore

```
Generate a comprehensive .dockerignore for:

Project type: [Python/Node.js/Go/etc.]
Framework: [Django/Next.js/etc.]
Additional patterns to exclude: [list any specific files/folders]
```

### Create Health Check

```
Create a health check for:

Application: [TYPE]
Health endpoint: [URL/PORT]
Expected response: [STATUS CODE/BODY]
Startup time: [APPROXIMATE]

Include:
- Dockerfile HEALTHCHECK
- Docker Compose healthcheck
- Verification command
```

### Generate Resource Limits

```
Recommend resource limits for:

Service: [DESCRIPTION]
Expected load: [CONCURRENT USERS/REQUESTS]
Available resources: [TOTAL CPU/MEMORY]
Other services on same host: [LIST]

Provide:
- CPU limits and reservations
- Memory limits and reservations
- PID limits
- Justification
```

### Create Seccomp Profile

```
Create a custom seccomp profile for:

Application type: [web server/database/etc.]
Required syscalls: [list any known requirements]
Security level: [restrictive/moderate/permissive]

Provide:
- Seccomp profile JSON
- Testing instructions
- Explanation of allowed syscalls
```

---

## Prompt Template Variables

Use these placeholders in prompts:

| Variable | Description |
|----------|-------------|
| `[LANGUAGE]` | Python, Node.js, Go, Rust, Java |
| `[FRAMEWORK]` | FastAPI, Django, Express, Next.js, Gin |
| `[PORT]` | Application port number |
| `[IMAGE]` | Base image name |
| `[VERSION]` | Version tag |
| `[SIZE]` | Image size in MB |
| `[TIME]` | Build time |
| `[PATH]` | File or directory path |
| `[ERROR]` | Error message |
| `[PLATFORM]` | CI/CD platform |
| `[REGISTRY]` | Container registry |

---

*Docker LLM Prompts | faion-infrastructure-engineer*
