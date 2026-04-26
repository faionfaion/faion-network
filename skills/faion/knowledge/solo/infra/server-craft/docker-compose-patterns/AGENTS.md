# Docker Compose Patterns

## Summary

Docker Compose V2 patterns for running stateful infrastructure services (PostgreSQL, Redis, RabbitMQ) on a single VPS alongside systemd application services. Bind database ports to `127.0.0.1` to prevent Docker from bypassing UFW. Every service referenced by `depends_on: condition: service_healthy` must have a `healthcheck` block — without it the condition is silently ignored. Use named volumes (not bind mounts) for all database data.

## Why

For solo developer VPS platforms, containerizing infrastructure (databases, brokers, caches) while running application code as systemd services gives the best of both worlds: reproducible infrastructure setup without Docker overhead in the hot path of Python/Node services. The specific pitfall that causes production incidents: Docker inserts iptables ACCEPT rules that bypass UFW, so a port bound to `0.0.0.0:5432` is reachable from the internet regardless of firewall rules.

## When To Use

- Running PostgreSQL, Redis, RabbitMQ, or monitoring tools on a single server
- Multi-service development stack where services need to discover each other by name
- Infrastructure that should survive application deploys (DB persists across `deploy.sh` runs)
- Adding optional services (monitoring, pgadmin) via compose profiles

## When NOT To Use

- Running application code (Python, Node.js apps) in containers when they are deployed via rsync — adds complexity without benefit
- Multi-host deployments — use Kubernetes or Docker Swarm
- When the application requires direct access to `/proc` or host namespaces

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | Service definition rules, network isolation, healthcheck requirements, volume types, resource limits, log rotation |
| `content/02-infra-stack.xml` | NERO-style infrastructure stack (postgres + redis + rabbitmq), profile patterns, environment variable precedence |

## Templates

| File | Purpose |
|------|---------|
| `templates/infra-stack.yml` | Ready-to-use postgres + redis + rabbitmq with healthchecks, named volumes, backend network |
| `templates/monitoring.yml` | Prometheus + Grafana + node-exporter as a profiles-gated monitoring stack |
