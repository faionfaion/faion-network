---
slug: firewall-management
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure UFW (Uncomplicated Firewall) with nftables backend on Ubuntu 24.
content_id: "e22fe5f3d04bf05d"
tags: [firewall, ufw, nftables, docker, security]
---
# Firewall Management with UFW on Ubuntu 24.04

## Summary

**One-sentence:** Configure UFW (Uncomplicated Firewall) with nftables backend on Ubuntu 24.

**One-paragraph:** Configure UFW (Uncomplicated Firewall) with nftables backend on Ubuntu 24.04 VPS: deny-by-default policies, service rules, SSH rate limiting, and Docker port binding to prevent UFW bypass. The critical rule: Docker publishes ports by binding to 0.0.0.0 which bypasses UFW — always bind Docker services to 127.0.0.1.

## Applies If (ALL must hold)

- Setting up a new VPS for the first time
- Adding a new service that listens on a port
- Auditing whether Docker services are accidentally exposed
- Restricting web traffic to Cloudflare IPs only
- Diagnosing unexpected port exposure

## Skip If (ANY kills it)

- Managed cloud environments with their own security groups (AWS SGs, GCP firewall rules) — use those instead of or in addition to UFW
- When iptables is managed by another tool (docker rootless mode, k8s) — verify no conflicts before enabling UFW
- Rate-limiting HTTP/HTTPS at the firewall level — use nginx limit_req for that; UFW rate limit is for SSH only

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
