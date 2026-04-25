# Agent Integration — Docker Compose (Infrastructure Engineer)

## When to use
- Defining multi-container application stacks: app + DB + cache + worker in a single compose file
- Provisioning shared infrastructure services on a VPS (PostgreSQL, Redis/Valkey, RabbitMQ, n8n) that multiple projects consume
- Setting up isolated per-project stacks with their own networks, volumes, and resource limits
- Local development environments that mirror production topology
- Rolling out infrastructure updates that require orchestrated service restarts with health-check ordering

## When NOT to use
- Single-container deployments — a plain `docker run` with a systemd unit is simpler and more observable
- Production at scale requiring multi-host orchestration — use Kubernetes or Docker Swarm
- Applications that require zero-downtime blue-green deploys — Compose lacks built-in traffic shifting; use Kubernetes or a load balancer pair
- Stateless functions or serverless workloads — container overhead is not worth it

## Where it fails / limitations
- `deploy.resources.limits` in standalone Compose (non-Swarm) requires Docker Engine 20.10+ with cgroups v2; older hosts silently ignore limits
- Named volumes persist after `docker compose down`; running `down -v` is destructive — data loss risk if accidentally run against production
- `container_name` prevents horizontal scaling (`--scale` flag fails); must be removed to scale a service
- Health check `start_period` must account for slow DB initialization; setting it too short causes dependency loops where the app fails before the DB is ready
- Bind mounts (`./src:/app`) in production create host-path coupling and permission mismatches between container user UID and host UID
- The `version:` field is obsolete and triggers a deprecation warning in Compose v2.x+ — remove it

## Agentic workflow
An infrastructure agent reads the existing compose files in `/opt/<project>/` to understand current service topology, generates or updates the `compose.yaml` with new services, validates with `docker compose config`, runs `docker compose up -d` and polls `docker compose ps` until all services reach `healthy` state. For shared infrastructure (DB, cache), the agent checks if the service already exists in the running stack before adding it, to avoid creating duplicate instances.

### Recommended subagents
- `bash-agent` — generates compose file, runs `docker compose config` validation, applies with `up -d`, polls health
- `monitoring-agent` — reads `docker stats` and `docker compose logs` after deployment to confirm resource usage is within budget

### Prompt pattern
```
Generate a Docker Compose file (compose.yaml, no version field) for the following stack:
- <service 1>: image <image>, port <host:container>, env from .env, healthcheck
- <service 2>: postgres:16-alpine, named volume, healthcheck, NOT exposed externally
- Network: custom bridge "app-network", DB on internal-only subnet
- Resource limits: app 512M RAM / 0.5 CPU, DB 1G RAM / 1.0 CPU
- Restart policy: unless-stopped for all services

Return the full compose.yaml and the deploy commands.
```

```
Validate the compose file and report all issues:
1. Run: docker compose config --quiet
2. Check for: version field (remove), bind mounts in prod (flag), missing healthchecks, no resource limits, hardcoded secrets in environment
Return a prioritized fix list.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `docker compose` | Primary Compose CLI (v2, built into Docker) | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| `docker compose config` | Validate and print merged compose config | built-in |
| `docker compose ps` | Show service status and health | built-in |
| `docker stats` | Live resource usage per container | built-in |
| `docker inspect` | Detailed container state including health check results | built-in |
| `ctop` | Terminal UI for container resource monitoring | `apt install ctop` / [github.com/bcicen/ctop](https://github.com/bcicen/ctop) |
| `lazydocker` | TUI for full Compose stack management | [github.com/jesseduffield/lazydocker](https://github.com/jesseduffield/lazydocker) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Docker Hub | SaaS | Yes — image pull | Public registry; use specific tags, never `latest` in production |
| GitHub Container Registry (ghcr.io) | SaaS | Yes — `docker pull` | Private images; requires `docker login ghcr.io` |
| Watchtower | OSS | Yes — Docker-based | Auto-updates containers when new images are pushed; use with care |
| Portainer | OSS | Yes — REST API + UI | Web UI to manage Compose stacks; API-driven deployments |
| Netdata | OSS | Yes — REST API | Container-level metrics with Docker integration |

## Templates & scripts
See `templates.md` for the full production compose template with health checks, network isolation, and resource limits.

Health-check poll script (inline, 15 lines):
```bash
#!/bin/bash
# wait-healthy.sh SERVICE [TIMEOUT_SECONDS]
SERVICE="${1:?Usage: $0 SERVICE}"
TIMEOUT="${2:-120}"
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$SERVICE" 2>/dev/null || echo "missing")
    [ "$STATUS" = "healthy" ] && { echo "$SERVICE is healthy"; exit 0; }
    echo "Waiting for $SERVICE (status: $STATUS)..."
    sleep 5
    ELAPSED=$((ELAPSED + 5))
done
echo "ERROR: $SERVICE did not become healthy within ${TIMEOUT}s"
exit 1
```

## Best practices
- Use specific image tags (e.g., `postgres:16.3-alpine`) never `latest` — unpinned tags cause silent breaking changes on `docker compose pull`
- Define explicit custom networks rather than relying on the default bridge — enables `internal: true` for DB networks that must not reach the internet
- Add `healthcheck` to every service and use `depends_on: condition: service_healthy` — prevents app from starting before DB is ready
- Set resource limits (`deploy.resources.limits`) from day one — a runaway container with no limit can starve the entire host
- Use `env_file: .env` for secrets, never hardcode in compose file — the compose file should be safe to commit
- Name volumes explicitly (`postgres-data:`) rather than using anonymous volumes — anonymous volumes are hard to identify and back up
- Use `restart: unless-stopped` for long-running services; avoid `always` which restarts even during intentional maintenance

## AI-agent gotchas
- **`docker compose down -v` is destructive.** Agents must never run this against production without explicit operator confirmation — it deletes all named volumes including DB data
- **Health check `start_period` is critical for slow-starting services.** Agents generating Compose files must account for PostgreSQL initialization time (first boot with no volume takes 10-20s longer) and set `start_period: 60s` for DB services
- **Resource limits require cgroups v2.** Agents applying compose files to older hosts may see limits silently ignored; verify with `docker info | grep "Cgroup Driver"`
- **Compose file validation (`docker compose config`) does not catch runtime errors.** A valid config can still fail on `up` if the image does not exist, a port is already bound, or a volume mount fails permissions
- **`container_name` blocks scale and causes conflicts.** If an agent generates a compose file with `container_name` and later tries `--scale`, it fails. Avoid `container_name` for scalable services
- **Network name collisions across projects.** Without a project name (`-p` flag or `COMPOSE_PROJECT_NAME`), two projects with the same network name create a conflict. Agents must set explicit project names or unique network names per project

## References
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Docker Compose best practices 2025](https://thinksys.com/devops/docker-best-practices/)
- [Awesome Compose examples](https://github.com/docker/awesome-compose)
- [lazydocker](https://github.com/jesseduffield/lazydocker)
