---
slug: multi-project-hosting
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Strategies for hosting 2-5 web projects on a single VPS: port allocation by 100-range convention with a /srv/port-registry.
content_id: "900d38477f6b4b37"
tags: [hosting, nginx, multi-project, port-allocation, vps]
---
# Multi-Project Hosting

## Summary

**One-sentence:** Strategies for hosting 2-5 web projects on a single VPS: port allocation by 100-range convention with a /srv/port-registry.

**One-paragraph:** Strategies for hosting 2-5 web projects on a single VPS: port allocation by 100-range convention with a /srv/port-registry.txt as single source of truth, nginx multi-domain reverse proxy with shared snippets, Cloudflare DNS and origin certificates, shared vs isolated PostgreSQL/Redis decision matrix, and resource budget planning.

## Applies If (ALL must hold)

- Adding a second project to an existing VPS (port allocation and nginx config needed)
- Configuring nginx for a new domain with SSL via Cloudflare origin cert
- Deciding whether to share PostgreSQL/Redis or isolate per project
- Auditing resource utilization to determine whether to split to a second server

## Skip If (ANY kills it)

- Single-project servers where isolation is not a concern
- Kubernetes/Swarm clusters — use cluster-native ingress instead
- Serverless or PaaS deployments (Vercel, Railway) — hosting is abstracted
- Projects with strict compliance requirements mandating physical isolation

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
