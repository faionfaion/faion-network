# Agent Integration — Docker Compose (CI/CD Engineer)

## When to use
- Defining the service stack that CI/CD pipelines spin up for integration and end-to-end tests (ephemeral Compose environments)
- Building application images as part of a pipeline (`docker compose build`) before pushing to a registry
- Running database migrations and smoke tests against a freshly composed stack in CI
- Parameterizing compose files with `compose.override.yaml` to switch between local dev, CI, and production configurations
- Using `docker compose watch` during development for file-change-triggered container reloads

## When NOT to use
- Production deployments where zero-downtime is required — Compose has no traffic shifting; use Kubernetes rolling updates or a reverse proxy flip
- Multi-host deployments in CI — Compose is single-host; use Kubernetes test clusters or Testcontainers for that scenario
- Workflows where only a single container is needed — `docker run` in the pipeline is simpler
- Teams with Kubernetes already in production — align CI environment with prod using `helm template` + `kubectl apply` rather than Compose

## Where it fails / limitations
- `docker compose down --volumes` in CI teardown removes test data but also any seeded fixtures that were expected to persist across test phases
- Compose service health checks in CI can time out if the CI runner is slow (shared runners with low CPU) — `start_period` must be generous
- `docker compose watch` requires Docker Desktop or a Docker daemon that supports the watch feature; not available on all CI hosts
- Image layers are not cached between CI runs unless the runner persists the Docker layer cache (requires explicit cache configuration in CI)
- The `--scale` flag in CI is useful for parallelizing workers but creates port conflicts if `ports:` is statically mapped — must use `expose:` instead for internal services
- `depends_on: condition: service_healthy` only waits for the health check to pass, not for the application to finish migrations or seeding

## Agentic workflow
A CI/CD agent generates or updates the `compose.yaml` and `compose.ci.yaml` override file, ensures all services have health checks and the app depends on DB health, generates the CI pipeline step that runs `docker compose -f compose.yaml -f compose.ci.yaml up -d --wait`, then runs tests against the composed stack, and tears down with `docker compose down -v` in the pipeline's cleanup step. The agent validates the compose file with `docker compose config` before committing it.

### Recommended subagents
- `bash-agent` — generates compose.ci.yaml override, validates with `docker compose config`, runs the test stack
- `ci-pipeline-agent` — generates GitHub Actions or GitLab CI step that uses the compose file for integration tests

### Prompt pattern
```
Generate a CI-specific Docker Compose override file (compose.ci.yaml) for a <stack> application with:
- No port bindings exposed to host (use expose: only)
- Health checks with generous start_period (60s) for slow CI runners
- DB initialized from seed file via init container
- App waits for DB health before starting
- No resource limits (CI runner manages this)
- All secrets passed via CI environment variables, not .env file

Return compose.ci.yaml and the CI pipeline step to bring it up, run tests, and tear down.
```

```
Given this GitHub Actions workflow, add a step that:
1. Starts the Docker Compose stack with `docker compose -f compose.yaml -f compose.ci.yaml up -d --wait`
2. Runs the test suite against the composed services
3. Always tears down with `docker compose down -v` even if tests fail (using `if: always()`)
Return the full updated workflow YAML.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `docker compose` | Manage multi-container test stacks in CI | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| `docker compose up --wait` | Start all services and wait for healthy state before returning | built-in (Compose v2.1+) |
| `docker compose config` | Validate merged compose files before CI run | built-in |
| `docker compose watch` | Hot-reload containers on file change (dev mode) | built-in (Compose v2.22+) |
| `docker buildx bake` | Build multiple images in parallel from compose file | [docs.docker.com/build/bake](https://docs.docker.com/build/bake/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — YAML workflow | Native Docker support; cache layers with `actions/cache` |
| GitLab CI | SaaS/OSS | Yes — YAML pipeline | Docker-in-Docker (dind) service for Compose; or use Kubernetes executor |
| Testcontainers | OSS | Yes — library API | Programmatic Compose-compatible container lifecycle from tests |
| GitHub Container Registry | SaaS | Yes — `docker push` | Store built images; pull in subsequent CI steps |
| Docker Build Cloud | SaaS | Yes — `docker buildx` | Remote build cache shared across runners |

## Templates & scripts
See `templates.md` for the full `compose.ci.yaml` override template and the GitHub Actions integration test job.

Compose CI teardown with volume cleanup (inline, always runs):
```yaml
# GitHub Actions step snippet
- name: Start test stack
  run: docker compose -f compose.yaml -f compose.ci.yaml up -d --wait

- name: Run integration tests
  run: pytest tests/integration/

- name: Tear down stack
  if: always()
  run: docker compose -f compose.yaml -f compose.ci.yaml down -v --remove-orphans
```

Compose config validation step (inline):
```bash
#!/bin/bash
# validate-compose.sh — run in CI before any docker compose up
set -euo pipefail
docker compose -f compose.yaml -f compose.ci.yaml config --quiet
echo "Compose config valid"
```

## Best practices
- Use `--wait` flag (`docker compose up -d --wait`) in CI — it blocks until all health checks pass, eliminating manual sleep or polling loops
- Split `compose.yaml` (base) and `compose.ci.yaml` (CI override) — keep production and CI concerns separate; the override only changes what CI needs (no port bindings, seed data)
- Run `docker compose config` as the first step in CI to catch YAML errors before spinning up containers
- Use `expose:` instead of `ports:` for internal services in CI — avoids host port conflicts when multiple CI jobs run concurrently on the same runner
- Always add `--remove-orphans` to `docker compose down` in CI teardown — prevents leftover containers from previous runs polluting the next run
- Cache Docker layers in CI using `docker buildx` with `--cache-to` and `--cache-from` registry mode — dramatically reduces build time
- Use `docker compose watch` in local dev only, not in CI — CI runs are one-shot; hot reload adds complexity without benefit

## AI-agent gotchas
- **`docker compose up -d --wait` requires Compose v2.1+.** Agents must verify the Compose version available on the CI runner; older runners may not have `--wait` and need an explicit health-check polling step
- **Concurrent CI jobs on shared runners cause port conflicts** if compose files use `ports:` mappings. Agents must generate CI compose overrides that use `expose:` only, letting Docker's internal networking handle connectivity
- **Teardown step must use `if: always()`.** Agents writing CI pipelines must ensure the `docker compose down -v` step runs even when tests fail — otherwise volumes accumulate across failed runs and disk fills up
- **Layer cache is not automatic.** Agents generating CI workflows must explicitly configure Docker layer caching (`actions/cache` with Docker buildx cache) — without it, every CI run rebuilds from scratch
- **`compose.ci.yaml` secrets from environment variables, not `.env`.** Agents must not copy the local `.env` file pattern into CI — secrets must come from CI environment variables (GitHub Secrets / GitLab CI variables) injected at pipeline run time

## References
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker Build Cloud](https://docs.docker.com/build/cloud/)
- [Testcontainers](https://testcontainers.com/)
- [GitHub Actions Docker layer cache](https://docs.docker.com/build/ci/github-actions/cache/)
- [Awesome Compose examples](https://github.com/docker/awesome-compose)
