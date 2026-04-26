# Docker Compose (CI/CD)

## Summary

Docker Compose patterns for CI/CD pipelines: `compose.ci.yaml` override that removes port bindings, sets generous `start_period` for slow CI runners, uses `docker compose up -d --wait` to block until all health checks pass, and always tears down with `docker compose down -v --remove-orphans` in an `if: always()` cleanup step. CI secrets come from environment variables, not `.env` files.

## Why

CI runners are slower than dev machines — health check `start_period` that works locally will time out on shared CI runners. Port bindings in CI cause conflicts when multiple jobs run concurrently on the same runner. `--wait` eliminates manual sleep/polling. Missing `if: always()` on teardown causes volumes to accumulate on failed runs, filling the runner disk.

## When To Use

- Spinning up integration test stacks in CI (app + DB + dependencies)
- Building application images in CI with `docker compose build` before pushing to registry
- Running database migrations and smoke tests against a freshly composed stack
- Parameterizing compose files with override files for local dev vs CI vs production configurations

## When NOT To Use

- Production deployments where zero-downtime is required — use Kubernetes rolling updates
- Multi-host deployments in CI — use Kubernetes test clusters or Testcontainers
- Pipelines needing only a single container — `docker run` in the pipeline is simpler
- Teams with Kubernetes already in production — align CI with prod using helm/kubectl

## Content

| File | What's inside |
|------|---------------|
| `content/01-ci-override.xml` | compose.ci.yaml pattern: no ports, generous start_period, expose-only internal services |
| `content/02-pipeline-integration.xml` | GitHub Actions step sequence: up --wait, run tests, always-teardown; layer cache setup |

## Templates

| File | Purpose |
|------|---------|
| `templates/compose.ci.yaml` | CI override: no port bindings, generous health timeouts, secrets from env vars |
| `templates/github-actions-step.yaml` | GitHub Actions job steps for compose-based integration tests |
