# Agent Integration — Docker Compose Patterns

## When to use
- Standing up infrastructure services (PostgreSQL, Redis, RabbitMQ) on a new VPS
- Adding a containerized backing service to an existing application stack
- Debugging a misbehaving Docker service (container keeps restarting, health check failing)
- Auditing a docker-compose.yml for security issues (ports bound to 0.0.0.0)
- Generating a compose file for a new project from a template

## When NOT to use
- Running application code in Docker on a single VPS — prefer systemd user services (less overhead, better log integration, simpler deploys)
- Multi-host orchestration — use Kubernetes or Docker Swarm instead
- CI/CD ephemeral environments — use per-job Docker runner instead
- When the service has no state and can be a one-liner systemd ExecStart

## Where it fails / limitations
- Docker manipulates iptables/nftables directly, bypassing UFW rules — a port bound without 127.0.0.1 is internet-accessible regardless of firewall config
- `deploy.resources` requires Compose V2; legacy `docker-compose` V1 ignores it silently
- Named volumes survive `docker compose down` but are deleted by `docker compose down -v` — agent must distinguish these commands precisely
- Health check `condition: service_healthy` only works with Compose V2 and a defined `healthcheck:` block; missing healthcheck causes `depends_on` to fall back to `service_started` silently
- Log rotation must be configured explicitly; default json-file driver grows unbounded on a busy VPS

## Agentic workflow
An agent can read an existing docker-compose.yml, validate it against this methodology's checklist (port binding, resource limits, health checks, log rotation), and emit a corrected version. For new stacks, the agent selects the appropriate service block from templates.md and assembles a compose file. The agent should always run `docker compose config` to validate the output before applying it. After applying, the agent checks `docker compose ps` and waits for all services to report healthy status before declaring success.

### Recommended subagents
- `faion-sdd-executor-agent` — execute a server-craft SDD task that includes deploying a compose stack as a subtask

### Prompt pattern
```
Read the docker-compose.yml at <path>. Check:
1. All ports are bound to 127.0.0.1, not 0.0.0.0.
2. Every service has healthcheck, resource limits, and log rotation.
3. depends_on uses condition: service_healthy where applicable.
Output a corrected file and list what was changed.
```

```
Generate a docker-compose.yml for PostgreSQL 16 + Redis 7 + RabbitMQ 3 (management).
Requirements: localhost-only ports, named volumes, health checks, json-file logging (max 10m × 3), resource limits (postgres: 2G RAM, redis: 256M, rabbitmq: 512M).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `docker compose` | V2 CLI plugin (built into Docker Engine 20.10+) | `apt install docker-ce` / [docs](https://docs.docker.com/compose/reference/) |
| `docker compose config` | Validate and print resolved compose file | Built-in |
| `docker compose ps` | List container states and health | Built-in |
| `docker compose top` | Show processes inside containers | Built-in |
| `docker volume ls / inspect / prune` | Volume management | Built-in |
| `lazydocker` | TUI for Docker management | `brew install lazydocker` / [GitHub](https://github.com/jesseduffield/lazydocker) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL (official image) | OSS | Yes | Use `pg_isready` healthcheck; pin minor version (e.g., `16.2-alpine`) |
| Redis (official image) | OSS | Yes | Use `redis-cli ping` healthcheck; enable AOF persistence if data matters |
| RabbitMQ management (official) | OSS | Yes | Management API on 15672 is useful for health checks; bind to 127.0.0.1 |
| Flower (mher/flower) | OSS | Partial | Celery monitoring UI; use `profiles: ["monitoring"]` to keep it optional |
| n8n | OSS | Yes | Self-hostable automation; run in Docker, expose via nginx reverse proxy |

## Templates & scripts
See templates.md for complete compose blocks per service type. Key inline patterns:

```yaml
# Minimal production-ready service block
services:
  postgres:
    image: postgres:16-alpine
    container_name: ${COMPOSE_PROJECT_NAME:-myapp}-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          memory: 2G

volumes:
  pgdata:
```

## Best practices
- Always bind ports to `127.0.0.1` — Docker bypasses UFW; `0.0.0.0` means internet-accessible
- Use `container_name` explicitly — generated names change on stack rename and break scripts
- Pin image versions to a specific minor tag (not `latest`) to avoid surprise upgrades
- Use `restart: unless-stopped` not `restart: always` — `always` restarts even on explicit `docker compose stop`
- Define health checks for every stateful service; use `condition: service_healthy` in `depends_on`
- Store secrets in `.env` (not in compose file); add `.env` to `.gitignore`
- Set `COMPOSE_PROJECT_NAME` in `.env` to namespace volumes and networks — prevents collisions on multi-project hosts
- Use `profiles:` for optional services (monitoring, debug tools) so they don't start with `docker compose up`
- Configure `logging.options.max-size` per service or globally in `/etc/docker/daemon.json`
- Never run `docker compose down -v` on production without explicit backup confirmation

## AI-agent gotchas
- Agents must distinguish `docker compose down` (safe) from `docker compose down -v` (destroys volumes) — always confirm before using `-v`
- `docker compose pull` followed by `docker compose up -d` causes zero-downtime replacement only if health checks are configured; without them, dependent services may start before the DB is ready
- The `deploy.resources` block is silently ignored by Docker Swarm mode's compose handling — agent must confirm target is plain Compose, not Swarm
- When editing a running stack, `docker compose up -d` only recreates services whose config changed — verify with `docker compose ps` after apply
- Port conflicts produce a generic error; agent should run `ss -tlnp | grep PORT` to identify the conflicting process before retrying
- Health check `start_period` must account for slow container startup (e.g., PostgreSQL initializing a new data directory can take 30-60s) — set conservatively

## References
- https://docs.docker.com/compose/reference/
- https://docs.docker.com/compose/compose-file/
- https://docs.docker.com/config/containers/logging/json-file/
- https://docs.docker.com/network/iptables/ (Docker and firewall interaction)
- https://github.com/jesseduffield/lazydocker
