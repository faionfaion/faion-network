# Docker Compose LLM Prompts

**AI Prompts for Multi-Container Orchestration Tasks (2025-2026)**

---

## Compose File Generation

### Create Full Stack Compose

```
Create a Docker Compose configuration for:

Application Stack:
- Application: [language/framework] on port [PORT]
- Database: [PostgreSQL/MySQL/MongoDB]
- Cache: [Redis/Memcached] (if needed)
- Worker: [Celery/Bull] (if needed)
- Reverse proxy: [nginx/traefik] (if needed)

Requirements:
1. Modern compose format (no version field, compose.yaml naming)
2. Health checks with depends_on conditions
3. Named volumes for persistence
4. Network isolation (frontend/backend with internal)
5. Resource limits (cpus, memory, pids)
6. Environment via .env file
7. Logging with rotation
8. Security hardening:
   - Non-root users (uid 1000)
   - Read-only filesystem
   - cap_drop ALL
   - no-new-privileges

Include:
- compose.yaml (production base)
- compose.override.yaml (development)
- .env.example
- .dockerignore

Output: Complete files with comments explaining each section.
```

### Create Microservices Compose

```
Create a Docker Compose for microservices architecture:

Services:
[LIST SERVICES AND THEIR RELATIONSHIPS]
Example:
- API Gateway (Kong/Traefik)
- User Service (port 8001)
- Order Service (port 8002)
- Payment Service (port 8003)
- Each service has its own database

Requirements:
1. Network segmentation per service
2. Internal networks for databases (internal: true)
3. API gateway for external access only
4. Health checks for all services
5. Service discovery via DNS
6. Centralized logging configuration
7. Resource limits per service type

Provide:
- Complete compose.yaml
- Network diagram (text-based)
- Service communication patterns
- Scaling considerations
```

### Migrate Legacy Compose

```
Migrate this legacy docker-compose.yml to modern 2025-2026 format:

[PASTE OLD DOCKER-COMPOSE.YML]

Changes needed:
1. Remove version field (obsolete)
2. Rename to compose.yaml
3. Add health checks to ALL services
4. Add depends_on with condition: service_healthy
5. Add resource limits (deploy.resources)
6. Configure logging with rotation
7. Add security options (cap_drop, read_only, no-new-privileges)
8. Use modern CLI format (docker compose)
9. Create separate networks for tiers
10. Mark backend networks as internal: true

Provide:
- Updated compose.yaml
- List of breaking changes
- Migration commands
- Verification steps
```

---

## Service Configuration

### Configure Service Health Checks

```
Create health check configurations for these services:

Services:
- [SERVICE 1]: [type, port, health endpoint]
- [SERVICE 2]: [type, port, health endpoint]
- [SERVICE 3]: [type, port, health endpoint]

For each service, provide:
1. healthcheck configuration in compose
2. Appropriate interval, timeout, start_period, retries
3. depends_on with condition for dependent services

Service types to handle:
- HTTP APIs: curl or wget to /health
- PostgreSQL: pg_isready
- MySQL: mysqladmin ping
- MongoDB: mongosh eval
- Redis: redis-cli ping
- RabbitMQ: rabbitmq-diagnostics check_running
- Elasticsearch: curl cluster health

Output: YAML healthcheck blocks for each service.
```

### Configure Resource Limits

```
Recommend resource limits for this application:

Services:
- [SERVICE 1]: [description, expected load]
- [SERVICE 2]: [description, expected load]
- [SERVICE 3]: [description, expected load]

Available host resources:
- CPUs: [NUMBER]
- Memory: [AMOUNT]

Requirements:
- Leave 20% headroom for system
- Account for burst traffic
- Prevent single service from exhausting resources

For each service, provide:
- cpus limit and reservation
- memory limit and reservation
- pids limit
- Justification for values

Output: deploy.resources configuration for each service.
```

### Configure Dependencies

```
Configure service dependencies for:

Services and their requirements:
- [SERVICE 1]: needs [SERVICE A, SERVICE B]
- [SERVICE 2]: needs [SERVICE A] (wait for healthy)
- [SERVICE 3]: runs after [SERVICE 1] completes

Dependency types needed:
1. service_healthy - wait until health check passes
2. service_started - just wait for container start
3. service_completed_successfully - wait for exit 0

Include:
- Init containers (migrations, setup)
- Circular dependency prevention
- Start order optimization

Output: depends_on configuration with conditions.
```

---

## Networking

### Design Network Architecture

```
Design Docker Compose network architecture for:

Application: [DESCRIPTION]

Components:
- [SERVICE 1]: needs external access
- [SERVICE 2]: needs external access
- [SERVICE 3]: internal only
- [SERVICE 4]: database (isolated)

Requirements:
- Zero trust between tiers
- Minimal port exposure
- Database not accessible from internet
- Service-to-service by DNS name

Provide:
1. Network definitions with drivers
2. Service network assignments
3. Network diagram (text)
4. Security rationale
```

### Debug Network Connectivity

```
Debug container networking issue:

Setup:
[DESCRIBE CONTAINER SETUP]

Problem:
[DESCRIBE - e.g., "service app cannot reach service db"]

compose.yaml:
[PASTE RELEVANT SECTIONS]

Error messages:
[PASTE ERRORS]

Provide:
1. Diagnostic commands to run
2. Common causes for this issue
3. Likely root cause
4. Solution
5. Verification steps
```

### Configure Network Segmentation

```
Configure network segmentation for three-tier architecture:

Tiers:
- DMZ: nginx, WAF (external access)
- Application: api, workers (internal)
- Data: postgres, redis (isolated)

Requirements:
- DMZ can reach Application
- Application can reach Data
- Data cannot reach DMZ
- No direct DMZ to Data

Provide:
1. Network definitions
2. Service assignments
3. Verification commands
4. Security explanation
```

---

## Volumes

### Design Volume Strategy

```
Design volume strategy for:

Application: [DESCRIPTION]

Data requirements:
- [DATA 1]: [type, size, persistence needs, backup frequency]
- [DATA 2]: [type, size, persistence needs, backup frequency]
- [DATA 3]: [type, size, persistence needs, backup frequency]

Questions to address:
1. Named volumes vs bind mounts
2. Read-only mounts for configs
3. tmpfs for temporary data
4. Backup approach

Provide:
1. Volume configuration
2. Mount strategy per data type
3. Backup script (if applicable)
4. Recovery procedure
```

### Debug Volume Permissions

```
Debug volume permission issue:

Problem:
[DESCRIBE - e.g., "container cannot write to mounted volume"]

Container configuration:
- User in container: [UID:GID]
- Volume mount: [MOUNT SPEC]
- Host path: [PATH]
- Host permissions: [ls -la output]

Provide:
1. Root cause analysis
2. Fix options:
   - Dockerfile changes
   - Compose changes
   - Host permission changes
3. Recommended solution
4. Best practice explanation
```

---

## Security

### Security Audit Compose File

```
Perform a security audit on this Docker Compose file:

[PASTE COMPOSE FILE]

Check for (2025-2026 standards):
1. Services running as root
2. Missing cap_drop: ALL
3. Missing no-new-privileges
4. Missing read_only filesystem
5. Privileged mode usage
6. Exposed database ports
7. Hardcoded secrets
8. Missing resource limits (DoS risk)
9. Default bridge network usage
10. Missing health checks

Provide:
- Risk assessment per finding (Critical/High/Medium/Low)
- Specific vulnerabilities found
- Remediation for each
- Hardened compose.yaml
```

### Create Security Baseline

```
Create a security baseline for Docker Compose deployment:

Environment: [development/staging/production]
Compliance: [CIS/NIST/PCI-DSS/SOC2] (if applicable)

Include:
1. Minimum security options per service
2. Network isolation requirements
3. Resource limits requirements
4. Secret management approach
5. Logging requirements
6. Health check requirements

Output:
- Security policy document
- Compliant compose.yaml template
- Verification checklist
```

### Configure Secrets Management

```
Configure secrets management for:

Secrets needed:
- [SECRET 1]: [description, rotation frequency]
- [SECRET 2]: [description, rotation frequency]
- [SECRET 3]: [description, rotation frequency]

Environment: [docker-compose/swarm/kubernetes]

Options to consider:
1. Docker secrets (Swarm mode)
2. Environment files (.env)
3. External vault (HashiCorp, AWS SM)

Provide:
1. Recommended approach
2. Configuration
3. Application access pattern
4. Rotation procedure
5. Security rationale
```

---

## Scaling

### Configure Horizontal Scaling

```
Configure horizontal scaling for:

Service: [SERVICE NAME]
Target replicas: [NUMBER]
Load balancer: [nginx/traefik/none]

Current compose.yaml:
[PASTE CURRENT CONFIG]

Requirements:
1. Remove container_name (scaling requirement)
2. Stateless service verification
3. Session handling (if applicable)
4. Load balancer configuration

Provide:
1. Updated compose.yaml
2. Load balancer configuration
3. Scale command
4. Verification steps
```

### Configure Rolling Updates

```
Configure rolling updates for production deployment:

Service: [SERVICE NAME]
Current replicas: [NUMBER]
Acceptable downtime: [ZERO/MINIMAL]

Requirements:
1. Start new before stopping old
2. Health check gates deployment
3. Rollback on failure

Provide:
1. deploy configuration (update_config, rollback_config)
2. Health check requirements
3. Deployment command
4. Rollback procedure
```

---

## Development Workflows

### Create Development Environment

```
Create development environment for:

Application: [DESCRIPTION]
Tech stack: [LANGUAGES/FRAMEWORKS]

Development needs:
- Hot reload
- Debug ports
- Local database access
- Email testing (mailhog)
- Database admin (pgadmin)

Provide:
1. compose.override.yaml
2. Debug configuration
3. Verification that code changes reflect immediately
4. Common development commands
```

### Create Test Environment

```
Create test environment for:

Application: [DESCRIPTION]
Test framework: [pytest/jest/etc.]

Requirements:
1. Isolated test database (ephemeral)
2. Test-specific environment variables
3. Parallel test support
4. CI/CD integration

Provide:
1. compose.test.yaml
2. Test database configuration
3. Test command
4. CI/CD integration example
```

---

## Troubleshooting

### Debug Service Startup Failure

```
Debug service startup failure:

Service: [NAME]
Exit code: [CODE]

Logs:
[PASTE LOGS]

compose.yaml:
[PASTE RELEVANT CONFIG]

Attempted:
[WHAT HAS BEEN TRIED]

Provide:
1. Diagnostic commands
2. Root cause analysis
3. Solution
4. Prevention tips
```

### Debug Health Check Failure

```
Debug failing health check:

Service: [NAME]
Health status: unhealthy

Health check configuration:
[PASTE HEALTHCHECK]

Logs:
[PASTE RELEVANT LOGS]

Provide:
1. Diagnostic steps
2. Common causes for this service type
3. Root cause analysis
4. Fixed health check
5. Verification commands
```

### Debug Resource Exhaustion

```
Debug resource exhaustion issue:

Symptoms:
[DESCRIBE - OOM, CPU throttling, etc.]

Current resource configuration:
[PASTE DEPLOY.RESOURCES]

docker stats output:
[PASTE STATS]

Application type: [DESCRIPTION]
Expected load: [DESCRIPTION]

Provide:
1. Resource usage analysis
2. Recommended limits
3. Application optimization suggestions
4. Monitoring setup recommendations
```

---

## Multi-File Composition

### Organize Multi-Environment Setup

```
Organize Compose files for multi-environment deployment:

Environments:
- Development (local)
- Testing (CI/CD)
- Staging
- Production

Current single file:
[PASTE CURRENT COMPOSE.YAML]

Requirements:
1. Base file with production-ready defaults
2. Override file for development (auto-merged)
3. Separate files for test, staging, prod
4. Environment-specific resource limits
5. Clear deployment commands

Provide:
1. File structure
2. Each compose file
3. Deployment commands per environment
4. Merge verification commands
```

---

## Quick Task Prompts

### Generate Environment File

```
Generate .env.example for:

Application: [DESCRIPTION]
Services: [LIST]

Include:
- All configurable values
- Sensible defaults where appropriate
- Comments explaining each variable
- Groups by category (App, Database, Redis, etc.)
```

### Generate Makefile

```
Generate Makefile for Docker Compose operations:

Application: [NAME]

Operations needed:
- Build (dev and prod)
- Start (dev, prod, with profiles)
- Stop (with and without volumes)
- Logs (all and per-service)
- Shell access (app and db)
- Testing
- Scaling
- Cleanup
- Validation

Include:
- Variables for customization
- Help target with descriptions
- Phony declarations
```

### Generate Health Checks

```
Generate health check configurations for:

Services:
- [SERVICE 1]: [type, port]
- [SERVICE 2]: [type, port]
- [SERVICE 3]: [type, port]

For each:
- Compose healthcheck block
- Appropriate timing (interval, timeout, start_period)
- Verification command
```

---

## Prompt Variables

Use these placeholders:

| Variable | Description |
|----------|-------------|
| `[APP_NAME]` | Application name |
| `[LANGUAGE]` | Python, Node.js, Go, etc. |
| `[FRAMEWORK]` | FastAPI, Next.js, Gin, etc. |
| `[PORT]` | Application port |
| `[DATABASE]` | PostgreSQL, MySQL, MongoDB |
| `[CACHE]` | Redis, Memcached |
| `[PROXY]` | nginx, traefik |
| `[ENVIRONMENT]` | dev, test, staging, prod |
| `[REPLICAS]` | Number of instances |

---

*Docker Compose LLM Prompts | faion-infrastructure-engineer*
