# Docker Compose (Infrastructure)

## Summary

Production-grade Docker Compose patterns for multi-container infrastructure stacks: no `version:` field, named volumes, custom networks with `internal: true` for database tiers, health checks on every service with `depends_on: condition: service_healthy`, resource limits via `deploy.resources`, and `restart: unless-stopped`. The `compose.yaml` file (not `docker-compose.yml`) is the modern canonical name.

## Why

Compose without health checks causes race conditions where the app starts before the database is ready. Without custom networks, all containers share the default bridge and databases are reachable from any container. Without resource limits, a runaway container starves the host. These three patterns prevent the most common production failures in Compose-based infrastructure.

## When To Use

- Defining multi-container application stacks (app + DB + cache + worker)
- Provisioning shared infrastructure services on a VPS (PostgreSQL, Redis, RabbitMQ)
- Setting up isolated per-project stacks with own networks, volumes, and resource limits
- Rolling out infrastructure updates requiring orchestrated service restarts with health-check ordering

## When NOT To Use

- Single-container deployments — `docker run` + systemd unit is simpler and more observable
- Production at scale requiring multi-host orchestration — use Kubernetes or Docker Swarm
- Zero-downtime blue-green deploys — Compose lacks traffic shifting; use Kubernetes or a load balancer pair
- Stateless functions or serverless workloads

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | Service structure, health checks, depends_on conditions, resource limits, restart policies |
| `content/02-networking.xml` | Custom bridge networks, internal networks for DB tier, network aliases, DNS resolution |
| `content/03-volumes-security.xml` | Named volumes, read-only filesystems, non-root users, capabilities, tmpfs for temp data |

## Templates

| File | Purpose |
|------|---------|
| `templates/compose.yaml` | Production compose file with health checks, network isolation, resource limits |
