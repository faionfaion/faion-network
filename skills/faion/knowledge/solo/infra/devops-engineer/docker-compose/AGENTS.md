---
slug: docker-compose
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Docker Compose V2 (`docker compose`) declaratively defines multi-container applications in YAML.
content_id: "c73dda5c7f775d91"
tags: [docker, compose, containers, orchestration, devops]
---
# Docker Compose

## Summary

**One-sentence:** Docker Compose V2 (`docker compose`) declaratively defines multi-container applications in YAML.

**One-paragraph:** Docker Compose V2 (`docker compose`) declaratively defines multi-container applications in YAML. Every service that is a `depends_on` target must define a `healthcheck`; without it the condition `service_healthy` provides no runtime ordering guarantee. Use named volumes for persistent data, bind port `127.0.0.1:PORT:PORT` to avoid Docker bypassing UFW, and omit the legacy `version:` field.

## Applies If (ALL must hold)

- Local development stacks with multiple services (db + cache + broker)
- Integration testing against real service dependencies
- Single-host staging or small production deployments (up to ~10 services)
- Running infrastructure services (PostgreSQL, Redis, RabbitMQ) alongside systemd application services
- Prototyping microservice topology before committing to Kubernetes

## Skip If (ANY kills it)

- Multi-host production at scale — use Kubernetes or Docker Swarm
- Rolling-update zero-downtime deployments — Compose restarts containers, it does not roll them
- When the team already has Helm/K8s manifests — adding Compose creates dual maintenance burden
- Enterprise secrets management — Compose secrets are limited to files; use Vault or AWS Secrets Manager

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/infra/devops-engineer/`
