# Docker Compose

## Summary

Docker Compose V2 (`docker compose`) declaratively defines multi-container applications in YAML. Every service that is a `depends_on` target must define a `healthcheck`; without it the condition `service_healthy` provides no runtime ordering guarantee. Use named volumes for persistent data, bind port `127.0.0.1:PORT:PORT` to avoid Docker bypassing UFW, and omit the legacy `version:` field.

## Why

Default `docker run` scripts are imperative and fragile — they do not capture dependencies, restart policy, or resource limits. Compose gives a single declarative file that an agent can validate (`docker compose config`), version in git, and replay identically. The `service_healthy` condition on `depends_on` eliminates race conditions on startup; without it, containers start immediately regardless of database readiness.

## When To Use

- Local development stacks with multiple services (db + cache + broker)
- Integration testing against real service dependencies
- Single-host staging or small production deployments (up to ~10 services)
- Running infrastructure services (PostgreSQL, Redis, RabbitMQ) alongside systemd application services
- Prototyping microservice topology before committing to Kubernetes

## When NOT To Use

- Multi-host production at scale — use Kubernetes or Docker Swarm
- Rolling-update zero-downtime deployments — Compose restarts containers, it does not roll them
- When the team already has Helm/K8s manifests — adding Compose creates dual maintenance burden
- Enterprise secrets management — Compose secrets are limited to files; use Vault or AWS Secrets Manager

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Service definition rules: healthchecks, network isolation, volume types, resource limits, log rotation |
| `content/02-examples.xml` | Full-stack example (app + postgres + redis + nginx + worker) and dev/prod override pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/base-service.yml` | Generic service block with healthcheck, resource limits, logging |
| `templates/postgres.yml` | PostgreSQL service with health check and named volume |
| `templates/redis.yml` | Redis service with persistence and health check |
| `templates/env.example` | `.env.example` with all common variable stubs |
| `templates/watch-block.yml` | `develop.watch` block for live reload (Compose v2.22+) |
