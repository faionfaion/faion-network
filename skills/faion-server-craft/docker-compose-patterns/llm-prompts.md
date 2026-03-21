# Docker Compose Patterns LLM Prompts

## Setup and Configuration

### Prompt: Create Docker Compose Stack

```
Create a Docker Compose stack for my application infrastructure.

Application type: [e.g., Python/Celery platform, Node.js API, etc.]
Services needed:
- Database: [PostgreSQL version, Redis version, MongoDB, etc.]
- Message broker: [RabbitMQ, Kafka, none]
- Cache: [Redis, Memcached, none]
- Monitoring: [Flower, pgAdmin, RedisInsight, none]
- Other: [Elasticsearch, MinIO, etc.]

Server specs:
- OS: [e.g., Ubuntu 24.04]
- RAM: [e.g., 30GB]
- CPU: [e.g., 16 cores]
- Disk: [e.g., 200GB SSD]

Requirements:
- Bind to localhost only (behind nginx): [Yes/No]
- Custom PostgreSQL tuning: [Yes/No, if yes describe workload]
- Resource limits: [Yes/No]
- Health checks: [Yes/No]
- Log rotation: [Yes/No]
- Environment from .env file: [Yes/No]

Provide:
1. Complete docker-compose.yml
2. .env template with all required variables
3. daemon.json for global Docker settings
4. Makefile with common operations
5. Custom configs (PostgreSQL tuning, Redis config)
6. Startup and verification commands
```

### Prompt: Add Service to Existing Stack

```
I need to add a new service to my existing Docker Compose stack.

Current docker-compose.yml:
[paste current file]

New service:
- Name: [e.g., elasticsearch]
- Image: [e.g., elasticsearch:8.12]
- Ports needed: [e.g., 9200, 9300]
- Volume for data: [Yes/No]
- Health check: [describe or leave for recommendation]
- Resource limits: [e.g., 2GB RAM, 2 CPU]
- Depends on: [other services]
- Environment variables: [list]

Provide:
1. Updated docker-compose.yml with the new service
2. New environment variables for .env
3. Verification that existing services are not affected
4. Integration testing steps
```

## Troubleshooting

### Prompt: Docker Compose Service Won't Start

```
A Docker Compose service is failing to start. Help me debug.

Service: [name]
docker-compose.yml (relevant section):
[paste service definition]

`docker compose ps` output:
[paste]

`docker compose logs service-name` output:
[paste last 50 lines]

`docker inspect container-name` (relevant sections):
[paste State and HostConfig]

Recent changes:
- [what changed before it broke, e.g., updated image, changed config]

Diagnose:
1. Parse error messages
2. Check configuration issues
3. Verify ports, volumes, permissions
4. Check resource constraints
5. Suggest specific fixes
```

### Prompt: Docker Compose Networking Issue

```
Services in my Docker Compose stack cannot communicate with each other.

docker-compose.yml:
[paste]

Symptom:
- Service A cannot reach Service B: [error message]
- `docker compose exec serviceA ping serviceB`: [result]

`docker network ls` output:
[paste]

`docker network inspect network-name` output:
[paste]

Diagnose the networking issue and provide a fix.
```

### Prompt: Docker Disk Space Issue

```
My server is running low on disk space due to Docker.

`df -h` output:
[paste]

`docker system df` output:
[paste]

`docker system df -v` output (top entries):
[paste]

Current cleanup strategy: [none / manual prune / scheduled]

Help me:
1. Identify what's consuming the most space
2. Safely reclaim space without losing important data
3. Set up automatic cleanup
4. Configure log rotation to prevent future issues
5. Recommend volume backup before cleanup
```

## Optimization

### Prompt: Tune PostgreSQL in Docker

```
Help me tune PostgreSQL running in Docker Compose for my workload.

Server specs:
- Total RAM: [e.g., 30GB]
- CPUs: [e.g., 16]
- Disk: [SSD/NVMe]
- Other services on server: [list with approximate memory usage]

PostgreSQL usage:
- Database size: [e.g., 5GB]
- Active connections: [typical count]
- Query pattern: [read-heavy / write-heavy / mixed]
- Largest tables: [approximate row counts]
- Use case: [e.g., AI platform storing conversations, analytics, etc.]

Current docker-compose.yml PostgreSQL service:
[paste]

Provide:
1. Tuned PostgreSQL command parameters (shared_buffers, work_mem, etc.)
2. Resource limits for the container
3. Volume configuration for optimal I/O
4. Recommended extensions
5. Monitoring queries to track performance
```

### Prompt: Optimize Docker Compose for Production

```
Review my Docker Compose setup for production readiness.

Current docker-compose.yml:
[paste complete file]

Current .env:
[paste, redact actual passwords]

Server: [OS, specs]
Traffic: [expected load]

Review for:
1. Security issues (exposed ports, hardcoded secrets, privileged containers)
2. Reliability (restart policies, health checks, dependencies)
3. Performance (resource limits, volume drivers, networking)
4. Logging (rotation, driver configuration)
5. Data safety (volume persistence, backup strategy)
6. Operational readiness (monitoring, update procedure)

Provide specific improvements with before/after comparisons.
```

## Migration and Updates

### Prompt: Migrate Docker Compose Between Servers

```
I need to migrate my Docker Compose stack to a new server.

Current server: [specs]
New server: [specs]

Docker Compose services:
[list services with their volumes]

Data to migrate:
- PostgreSQL database: [size]
- Redis data: [size]
- Other volumes: [list with sizes]

Provide a zero-downtime (or minimum-downtime) migration plan:
1. Pre-migration preparation on new server
2. Data backup and transfer
3. DNS / IP cutover strategy
4. Verification on new server
5. Rollback plan
6. Post-migration cleanup
```

### Prompt: Upgrade Docker Compose Service

```
I need to upgrade a service in my Docker Compose stack.

Service: [e.g., PostgreSQL]
Current version: [e.g., 15]
Target version: [e.g., 16]

Current docker-compose.yml:
[paste relevant service]

Data volume: [volume name]
Database size: [approximate]

Is this a major version upgrade: [Yes/No]
Application compatibility verified: [Yes/No]

Provide:
1. Pre-upgrade backup procedure
2. Step-by-step upgrade process
3. Data migration steps (if major version)
4. Rollback procedure
5. Post-upgrade verification
6. Application changes needed (if any)
```
