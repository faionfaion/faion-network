# Agent Integration — Docker Compose

## When to use
- Spinning up local multi-service development stacks (db + api + cache + worker)
- Running integration tests against real service dependencies in CI
- Single-host staging or small production deployments (< 5 services, 1 server)
- Prototyping a microservice architecture before committing to Kubernetes
- Replacing ad-hoc `docker run` scripts with declarative, version-controlled stacks

## When NOT to use
- Multi-host production at scale — use Kubernetes or Docker Swarm instead
- Service mesh requirements (mTLS, circuit breakers) — Compose has no built-in support
- Deployments requiring rolling updates with zero downtime — Compose restarts containers, it does not roll them
- When the team already has Helm/K8s manifests — adding Compose creates dual maintenance burden
- Secrets management at enterprise scale — Compose secrets are limited to files; use Vault or AWS Secrets Manager

## Where it fails / limitations
- `depends_on` with `condition: service_healthy` only works if the service defines a `healthcheck` block; missing healthcheck causes immediate start regardless
- `docker compose watch` (live reload) requires Compose v2.22+ and explicit `develop.watch` block in the file
- Compose does not manage DNS beyond the internal project network; cross-project service discovery requires shared networks or host networking
- Volume bind mounts on macOS/Windows have significant I/O performance overhead compared to Linux — avoid for write-heavy workloads
- Compose profiles are not recursive; a service in profile A does not automatically pull in dependencies that are only defined under profile B

## Agentic workflow
An agent receives a service topology description (e.g., "Django + PostgreSQL + Redis + Celery") and generates a complete `docker-compose.yml` with health checks, named volumes, and environment variable stubs. A second agent pass validates the file by running `docker compose config` and checks for common pitfalls (missing healthchecks on depended-upon services, hard-coded secrets in environment blocks). Deployment agents can call `docker compose up -d --build` and poll `docker compose ps` to confirm all services reach the `running (healthy)` state before declaring success.

### Recommended subagents
- `faion-knowledge` (infra/server-craft/deploy-scripts) — integrates Compose into the workspace/runtime deploy pattern
- `faion-knowledge` (infra/server-craft/systemd-user-services) — wraps `docker compose up` in a systemd user service for boot persistence
- `faion-knowledge` (infra/server-craft/kernel-tuning) — tunes `vm.max_map_count` and file descriptors required by containerized workloads

### Prompt pattern
```
Generate a docker-compose.yml for: <service list>.
Requirements:
- No version: field (Compose v2 format)
- healthcheck defined for every service that is a depends_on target
- All secrets via environment variables referencing a .env file (no hard-coded values)
- Named volumes for all persistent data
- Internal-only backend network; expose only ports that need external access
Output the file and a matching .env.example.
```

```
Run `docker compose config` on the attached compose file and fix any validation errors.
Then check: (1) every depends_on target has a healthcheck, (2) no plaintext secrets in environment blocks,
(3) all ExecStart paths are absolute. Return the corrected file.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `docker compose` | Core orchestration CLI (v2, bundled with Docker Desktop / Engine 24+) | https://docs.docker.com/compose/reference/ |
| `docker compose config` | Validate and merge compose files | Built-in |
| `docker compose watch` | Live file-sync hot reload for development | Requires `develop.watch` block in compose file |
| `docker scout` | Vulnerability scanning for images | `docker scout cves <image>` |
| `hadolint` | Dockerfile linter | `brew install hadolint` or `docker run hadolint/hadolint` |
| `compose-viz` | Generate architecture diagrams from compose files | `pip install compose-viz` |
| `ctop` | Real-time container resource monitoring | https://github.com/bcicen/ctop |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Docker Hub | SaaS | Yes (REST API) | Image registry; agents can pull/push via `docker` CLI |
| GitHub Container Registry | SaaS | Yes (CLI) | Free for public images; auth via `docker login ghcr.io` |
| Portainer | OSS (+ SaaS) | Yes (REST API) | Web UI + API for managing Compose stacks on a server |
| Watchtower | OSS | Partial | Auto-updates running containers from new image tags; configure carefully in prod |
| Traefik | OSS | Yes (labels in compose) | Reverse proxy with automatic HTTPS; integrates natively via Docker labels |
| n8n | OSS (Docker) | Yes | Workflow automation; standard Docker Compose deployment pattern |

## Templates & scripts
See `templates.md` for full stack templates (Django+PG+Redis, Node+Mongo, FastAPI+Celery).

```bash
#!/bin/bash
# health-wait.sh — wait until all compose services are healthy
# Usage: ./health-wait.sh [project-dir] [timeout-seconds]
DIR="${1:-.}"
TIMEOUT="${2:-60}"
ELAPSED=0
cd "$DIR"
while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  UNHEALTHY=$(docker compose ps --format json 2>/dev/null \
    | python3 -c "import sys,json; [print(s['Name']) for s in [json.loads(l) for l in sys.stdin] if s.get('Health','') not in ('healthy','')]" \
    2>/dev/null | wc -l)
  [ "$UNHEALTHY" -eq 0 ] && echo "All services healthy" && exit 0
  echo "Waiting... ($UNHEALTHY unhealthy) ${ELAPSED}s"
  sleep 5; ELAPSED=$((ELAPSED+5))
done
echo "TIMEOUT: services not healthy after ${TIMEOUT}s" && exit 1
```

## Best practices
- Never put `version:` at the top of compose files — modern Compose (v2.x) ignores it; older tools reject valid files because of version mismatches
- Define `healthcheck` on every service that another service depends on with `condition: service_healthy`; otherwise `depends_on` provides no ordering guarantee at runtime
- Use override files (`docker-compose.override.yml`) for developer-local settings (volume bind mounts, debug ports) so the base file stays production-safe
- Pin image versions with a digest (`image: postgres:16.2@sha256:...`) in production; `latest` tags silently break on upstream changes
- Keep `.env` out of git; commit `.env.example` with all variable names and safe placeholder values
- Use named volumes (not bind mounts) for database data in production to avoid permission and performance issues
- Run `docker compose down -v` only intentionally — `-v` deletes named volumes including database data

## AI-agent gotchas
- Agents must run `docker compose config` to validate generated files before attempting `docker compose up`; invalid YAML causes silent failures with confusing error messages
- `docker compose exec` requires the service to already be running; agents sometimes call it immediately after `up -d` before the container starts — add a health-wait step
- Agents will omit `--no-deps` flag when rebuilding a single service, causing unnecessary rebuilds of dependencies; be explicit in prompts
- File paths in `volumes` bind mounts must be absolute or use `./` prefix; agents often output bare relative paths that fail on Linux
- `docker compose logs` without `-f` exits immediately; agents waiting for log output must use `--tail` with a specific count or check exit codes from health endpoints instead

## References
- https://docs.docker.com/compose/
- https://docs.docker.com/compose/compose-file/
- https://docs.docker.com/compose/how-tos/production/
- https://docs.docker.com/compose/how-tos/file-watch/
- https://github.com/compose-spec/compose-spec/blob/master/spec.md
