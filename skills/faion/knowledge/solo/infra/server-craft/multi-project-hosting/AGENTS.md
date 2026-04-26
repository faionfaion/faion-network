# Multi-Project Hosting

## Summary

Strategies for hosting 2-5 web projects on a single VPS: port allocation by 100-range convention with a /srv/port-registry.txt as single source of truth, nginx multi-domain reverse proxy with shared snippets, Cloudflare DNS + origin certificates, shared vs isolated PostgreSQL/Redis decision matrix, and resource budget planning.

## Why

Adding a second project to a server without a port convention creates conflicts. Without a registry, agents and humans lose track of what's bound where. nginx server blocks provide cheap domain isolation without separate servers. Shared PostgreSQL/Redis is the right trade-off for solo devs at 2-5 projects: lower resource use, simpler backups, acceptable blast radius.

## When To Use

- Adding a second project to an existing VPS (port allocation + nginx config needed)
- Configuring nginx for a new domain with SSL via Cloudflare origin cert
- Deciding whether to share PostgreSQL/Redis or isolate per project
- Auditing resource utilization to determine whether to split to a second server

## When NOT To Use

- Single-project servers where isolation is not a concern
- Kubernetes/Swarm clusters — use cluster-native ingress instead
- Serverless or PaaS deployments (Vercel, Railway) — hosting is abstracted
- Projects with strict compliance requirements mandating physical isolation

## Content

| File | What's inside |
|------|---------------|
| `content/01-port-allocation.xml` | 100-port range convention, port-registry.txt format, per-project directory layout |
| `content/02-nginx.xml` | Multi-domain server block pattern, shared snippets, enable/test/reload workflow |
| `content/03-shared-services.xml` | Shared vs isolated decision matrix, per-project PostgreSQL databases, Redis DB number allocation |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx-site.conf` | Generic nginx server block template with HTTP redirect, SSL, proxy, WebSocket |
| `templates/port-registry.txt` | Port allocation registry with format and example entries |
| `templates/setup-project.sh` | Create runtime dirs, .env, systemd service, update port registry for a new project |
| `templates/add-database.sh` | Create PostgreSQL database + user in shared Docker instance |
