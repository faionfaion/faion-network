# Docker Compose LLM Prompts

**AI assistant prompts for Docker Compose tasks**

---

## Prompt: Create Docker Compose Configuration

```
Create a Docker Compose configuration for a [STACK_TYPE] application.

Requirements:
- Application: [APP_TYPE] (e.g., Node.js, Python/Django, Go)
- Database: [DB_TYPE] (e.g., PostgreSQL, MySQL, MongoDB)
- Cache: [CACHE_TYPE] (e.g., Redis, Memcached, none)
- Additional services: [SERVICES] (e.g., Nginx, Celery, RabbitMQ)
- Environment: [ENV] (development/production)

Include:
1. Proper health checks for all services
2. depends_on with service_healthy conditions
3. Named volumes for persistent data
4. Separate networks (frontend/backend)
5. Resource limits for production
6. Environment variable management via .env file
7. Security hardening (non-root user, read-only where possible)

Output:
- docker-compose.yml
- docker-compose.override.yml (if development)
- Sample .env file
```

---

## Prompt: Add Health Checks

```
Add health checks to this Docker Compose service:

```yaml
[PASTE_SERVICE_CONFIG]
```

Service type: [SERVICE_TYPE] (e.g., web app, database, cache, queue)
Health endpoint: [ENDPOINT] (e.g., /health, /api/health, none)

Requirements:
- Appropriate test command for the service type
- Reasonable interval, timeout, retries values
- start_period for services with slow startup
- Integration with depends_on conditions
```

---

## Prompt: Configure Service Dependencies

```
Configure proper service dependencies for this Docker Compose setup:

```yaml
[PASTE_COMPOSE_CONFIG]
```

Startup order requirements:
1. [DB] must be ready before [APP]
2. [MIGRATIONS] must complete before [APP] starts
3. [CACHE] should be available but is optional
4. [WORKER] needs both [DB] and [QUEUE]

Use:
- service_healthy for databases and caches
- service_completed_successfully for migrations
- required: false for optional dependencies
```

---

## Prompt: Network Architecture

```
Design the network architecture for this Docker Compose application:

Services:
- [LIST_SERVICES]

Requirements:
- Public-facing services: [PUBLIC_SERVICES]
- Internal-only services: [INTERNAL_SERVICES]
- Service aliases needed: [ALIASES]
- External network integration: [YES/NO]

Output:
- Network definitions
- Service network assignments
- Service aliases configuration
- Explanation of traffic flow
```

---

## Prompt: Volume Strategy

```
Design volume strategy for this Docker Compose application:

Data requirements:
- [SERVICE_1]: [DATA_TYPE] (persistent/ephemeral)
- [SERVICE_2]: [DATA_TYPE]
- Shared data between: [SERVICE_A, SERVICE_B]

Development needs:
- Hot reload for: [SERVICES]
- Config files to mount: [FILES]

Output:
- Named volume definitions
- Bind mount configurations
- tmpfs for ephemeral data
- Backup considerations
```

---

## Prompt: Production Hardening

```
Harden this Docker Compose configuration for production:

```yaml
[PASTE_COMPOSE_CONFIG]
```

Apply:
1. Security best practices:
   - Drop capabilities
   - Read-only filesystem
   - No-new-privileges
   - Non-root user

2. Resource management:
   - CPU limits
   - Memory limits
   - Proper reservations

3. Operational excellence:
   - Restart policies
   - Logging configuration
   - Graceful shutdown

4. Network security:
   - Internal networks where appropriate
   - Minimal port exposure
```

---

## Prompt: Development to Production

```
Convert this development Docker Compose to production-ready:

```yaml
[PASTE_DEV_COMPOSE]
```

Changes needed:
1. Remove development-only features (hot reload, debug ports)
2. Add health checks
3. Configure proper restart policies
4. Set resource limits
5. Harden security
6. Configure proper logging
7. Use versioned images (not :latest)

Output:
- docker-compose.yml (base)
- docker-compose.prod.yml (production overlay)
- Deployment commands
```

---

## Prompt: Troubleshoot Compose Issues

```
Help troubleshoot this Docker Compose issue:

Error message:
```
[PASTE_ERROR]
```

Compose file:
```yaml
[PASTE_COMPOSE_CONFIG]
```

Context:
- Running command: [COMMAND]
- Docker version: [VERSION]
- OS: [OS]

Provide:
1. Likely cause of the error
2. Diagnostic commands to run
3. Solution steps
4. Prevention measures
```

---

## Prompt: Add Monitoring Stack

```
Add monitoring to this Docker Compose application:

```yaml
[PASTE_COMPOSE_CONFIG]
```

Monitoring requirements:
- Metrics collection: [YES/NO] (Prometheus)
- Dashboards: [YES/NO] (Grafana)
- Logging: [YES/NO] (ELK/Loki)
- Alerting: [YES/NO] (Alertmanager)

Application exposes:
- Metrics endpoint: [ENDPOINT or NONE]
- Log format: [JSON/TEXT]

Output:
- Additional services for monitoring
- Application service modifications
- Network configuration
- Sample Prometheus/Grafana configs
```

---

## Prompt: Microservices Setup

```
Create Docker Compose for microservices architecture:

Services:
1. [SERVICE_1]: [DESCRIPTION]
2. [SERVICE_2]: [DESCRIPTION]
3. [SERVICE_N]: [DESCRIPTION]

Communication:
- Sync: [HTTP/gRPC]
- Async: [QUEUE_TYPE] (RabbitMQ/Redis/Kafka)

Shared infrastructure:
- Database strategy: [SHARED/PER_SERVICE]
- Service discovery: [METHOD]
- API Gateway: [YES/NO]

Include:
- Service definitions with health checks
- Network isolation
- Inter-service communication
- Database per service (if applicable)
- Message queue configuration
```

---

## Prompt: CI/CD Integration

```
Create Docker Compose configuration for CI/CD pipeline:

Pipeline stages:
1. Build
2. Test (unit, integration)
3. E2E testing
4. Deploy

Requirements:
- Test database setup
- Test data seeding
- Service isolation for parallel tests
- Cleanup between runs

Environment:
- CI platform: [GITHUB_ACTIONS/GITLAB_CI/JENKINS]
- Test framework: [FRAMEWORK]

Output:
- docker-compose.test.yml
- CI configuration snippets
- Test data management strategy
```

---

## Prompt: Migrate from docker-compose v2 to v3+

```
Migrate this legacy docker-compose.yml to modern format:

```yaml
[PASTE_LEGACY_CONFIG]
```

Update:
1. Remove deprecated version field
2. Convert links to networks
3. Update volume syntax
4. Add health checks
5. Convert depends_on to long syntax with conditions
6. Add deploy section for resource management
7. Apply current best practices
```

---

## Quick Prompts

### Generate Health Check

```
Generate health check for [SERVICE_TYPE] running on port [PORT].
Protocol: [HTTP/TCP/SHELL]
Health endpoint: [ENDPOINT]
```

### Add Service

```
Add [SERVICE_TYPE] service to existing compose file.
Image: [IMAGE:TAG]
Dependencies: [SERVICES]
Environment variables: [VARS]
Persistent data: [YES/NO]
```

### Optimize Compose

```
Optimize this Docker Compose for:
- [ ] Faster builds
- [ ] Smaller images
- [ ] Better caching
- [ ] Reduced network overhead
- [ ] Lower resource usage

[PASTE_COMPOSE_CONFIG]
```

### Security Audit

```
Audit this Docker Compose configuration for security issues:

[PASTE_COMPOSE_CONFIG]

Check for:
- Exposed secrets
- Excessive privileges
- Missing resource limits
- Insecure configurations
- Network exposure
```

---

*Docker Compose LLM Prompts | faion-cicd-engineer*
