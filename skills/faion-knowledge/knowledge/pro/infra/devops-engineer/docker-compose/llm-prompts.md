# Docker Compose LLM Prompts

Prompts for generating and reviewing Docker Compose configurations.

## Generation Prompts

### New Project Setup

```
Generate a production-ready docker-compose.yml for a [STACK] application.

Requirements:
- Services: [LIST SERVICES - e.g., web app, PostgreSQL, Redis]
- Environment: [dev/staging/production]
- Features needed: [health checks, logging, profiles, etc.]

Include:
1. Health checks for all services
2. Proper depends_on with conditions
3. Resource limits
4. Network isolation (frontend/backend)
5. Named volumes for persistence
6. Logging configuration
7. Environment variables with sensible defaults

Follow 2025-2026 best practices:
- No `version:` field
- Use `condition: service_healthy` in depends_on
- Configure `docker compose watch` for development
```

### Development Override

```
Create a docker-compose.override.yml for local development.

Base compose file: [DESCRIBE OR PASTE]

Requirements:
- Enable hot reload/live sync
- Expose database ports for local tools
- Add debug ports
- Include development tools (mailhog, adminer, etc.)
- Use profiles for optional services
- Configure watch for 2025 style live reload
```

### Production Hardening

```
Review and harden this docker-compose.yml for production:

[PASTE COMPOSE FILE]

Check for:
1. Hardcoded secrets (move to .env)
2. Missing health checks
3. Missing resource limits
4. Exposed database ports
5. Missing restart policies
6. Bind mounts instead of named volumes
7. Missing logging configuration
8. Network isolation
9. Security best practices 2025-2026
```

### Service Addition

```
Add a [SERVICE NAME] service to this docker-compose.yml:

[PASTE COMPOSE FILE]

Requirements:
- Health check
- Proper networking
- Volume for persistence (if needed)
- Environment variables
- Resource limits
- Profile (if optional)
- Integration with existing services
```

## Review Prompts

### Security Audit

```
Perform a security audit on this docker-compose.yml:

[PASTE COMPOSE FILE]

Check:
1. Are secrets hardcoded?
2. Are containers running as root?
3. Are unnecessary ports exposed?
4. Is the backend network isolated?
5. Are read-only mounts used where possible?
6. Are images from trusted sources?
7. Are there any privilege escalation risks?

Provide:
- List of issues found
- Severity rating for each
- Remediation steps
```

### Best Practices Review

```
Review this docker-compose.yml against 2025-2026 best practices:

[PASTE COMPOSE FILE]

Check:
1. Version field (should be absent or 3.9+)
2. Health checks defined
3. depends_on with conditions
4. Resource limits
5. Network isolation
6. Named volumes
7. Logging configuration
8. Restart policies
9. Environment variable handling
10. Profile usage for optional services

Rate: Poor / Fair / Good / Excellent
Provide specific improvements.
```

### Performance Review

```
Analyze this docker-compose.yml for performance optimization:

[PASTE COMPOSE FILE]

Check:
1. Resource allocation (over/under provisioned?)
2. Build caching opportunities
3. Volume mount performance
4. Network configuration
5. Logging driver impact
6. Health check intervals

Suggest optimizations for:
- Faster startup
- Better resource utilization
- Improved container health monitoring
```

## Migration Prompts

### To Kubernetes

```
Convert this docker-compose.yml to Kubernetes manifests:

[PASTE COMPOSE FILE]

Generate:
1. Deployments for each service
2. Services for networking
3. ConfigMaps for environment
4. Secrets for sensitive data
5. PersistentVolumeClaims for storage
6. Ingress for external access

Maintain:
- Health check behavior
- Resource limits
- Network isolation
- Volume mounts
```

### Version Upgrade

```
Upgrade this docker-compose.yml to follow 2025-2026 standards:

[PASTE COMPOSE FILE]

Changes needed:
1. Remove `version:` field if present
2. Update `depends_on` to use conditions
3. Add `docker compose watch` configuration
4. Review and update health checks
5. Add resource limits if missing
6. Implement profiles for optional services
7. Update image versions to latest stable
```

## Troubleshooting Prompts

### Debug Container Issues

```
Debug this docker-compose issue:

Compose file:
[PASTE COMPOSE FILE]

Error/Symptom:
[DESCRIBE THE ISSUE]

Logs (if available):
[PASTE RELEVANT LOGS]

Analyze:
1. Identify root cause
2. Check configuration errors
3. Verify dependency order
4. Check network connectivity
5. Verify volume mounts
6. Check environment variables

Provide fix and explanation.
```

### Health Check Failures

```
My service health checks are failing:

Service configuration:
[PASTE SERVICE CONFIG]

Health check output:
[PASTE OUTPUT]

Container logs:
[PASTE LOGS]

Help me:
1. Understand why health check fails
2. Fix the health check configuration
3. Ensure proper startup timing
4. Verify the health endpoint works
```

## Specific Stack Prompts

### Node.js/Next.js

```
Create a docker-compose.yml for a Next.js application:

Stack:
- Next.js (App Router)
- PostgreSQL
- Redis (for caching)
- Optional: Prisma migrations service

Features:
- Development hot reload with docker compose watch
- Production build stage
- Database migrations on startup
- Health checks for all services
```

### Python/Django

```
Create a docker-compose.yml for a Django application:

Stack:
- Django + Gunicorn
- PostgreSQL
- Redis
- Celery worker + beat
- Nginx

Features:
- Static file serving
- Media file storage
- Database migrations
- Celery task queue
- Development vs production configs
```

### Go/Rust Microservices

```
Create a docker-compose.yml for a Go/Rust microservice:

Stack:
- Go/Rust API service
- PostgreSQL
- Redis
- Optional: gRPC services

Features:
- Multi-stage build (small production image)
- Health checks with native binary
- Graceful shutdown handling
- Hot reload in development (air/cargo-watch)
```

## Template Request Format

```
I need a Docker Compose configuration for:

Project type: [web app / API / microservices / data pipeline / etc.]
Tech stack: [frameworks, languages]
Services needed: [list all services]
Environment: [development / staging / production]

Special requirements:
- [requirement 1]
- [requirement 2]

Constraints:
- [constraint 1]
- [constraint 2]

Please provide:
1. Main docker-compose.yml
2. Development override (if dev environment)
3. Production override (if production)
4. .env.example
5. Key commands for common operations
```
