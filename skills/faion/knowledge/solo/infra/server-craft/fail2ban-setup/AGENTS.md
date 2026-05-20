---
slug: fail2ban-setup
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Dynamic IP banning layer for Ubuntu 24.
content_id: "3d66ec287daaeff7"
tags: [fail2ban, security, firewall, nftables, ubuntu]
---
# fail2ban Setup for Ubuntu 24.04

## Summary

**One-sentence:** Dynamic IP banning layer for Ubuntu 24.

**One-paragraph:** Dynamic IP banning layer for Ubuntu 24.04 servers using nftables backend and systemd journal log source: SSH jail (maxretry 3), nginx jails (botsearch, limit-req, http-auth), custom application filters, recidive jail for week-long all-ports bans on repeat offenders, and Cloudflare IP whitelisting. Configuration exclusively via drop-in files in jail.d/ and filter.d/ — never edit jail.conf directly.

## Applies If (ALL must hold)

- After SSH hardening — fail2ban is the dynamic complement to static firewall rules
- When adding any publicly exposed service (nginx, mail server) — add a jail for that service
- When nginx logs show repeated scanner traffic for the same IP — verify filter match, then enable jail
- Deploying behind Cloudflare — configure real-IP extraction so the actual attacker IP is banned

## Skip If (ANY kills it)

- Servers behind a private VPN where SSH is not reachable from the public internet
- Kubernetes pods / Docker containers logging to Docker log driver (not a file fail2ban can tail)
- As a substitute for SSH key-only auth — it is a complement, not a replacement
- Cloudflare Workers or serverless — no server-level log to monitor

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
