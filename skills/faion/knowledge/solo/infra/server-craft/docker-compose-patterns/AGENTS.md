---
slug: docker-compose-patterns
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Docker Compose V2 patterns for running stateful infrastructure services (PostgreSQL, Redis, RabbitMQ) on a single VPS alongside systemd application services.
content_id: "e974483129e23915"
tags: [docker, docker-compose, infrastructure, vps, postgres]
---
# Docker Compose Patterns

## Summary

**One-sentence:** Docker Compose V2 patterns for running stateful infrastructure services (PostgreSQL, Redis, RabbitMQ) on a single VPS alongside systemd application services.

**One-paragraph:** Docker Compose V2 patterns for running stateful infrastructure services (PostgreSQL, Redis, RabbitMQ) on a single VPS alongside systemd application services. Bind database ports to 127.0.0.1 to prevent Docker from bypassing UFW. Every service referenced by depends_on: condition: service_healthy must have a healthcheck block — without it the condition is silently ignored. Use named volumes (not bind mounts) for all database data.

## Applies If (ALL must hold)

- Running PostgreSQL, Redis, RabbitMQ, or monitoring tools on a single server.
- Multi-service development stack where services need to discover each other by name.
- Infrastructure that should survive application deploys (DB persists across deploy.sh runs).
- Adding optional services (monitoring, pgadmin) via compose profiles.

## Skip If (ANY kills it)

- Running application code (Python, Node.js apps) in containers when they are deployed via rsync — adds complexity without benefit.
- Multi-host deployments — use Kubernetes or Docker Swarm.
- When the application requires direct access to /proc or host namespaces.

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

- parent skill: `solo/infra/server-craft/`
