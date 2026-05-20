---
slug: server-init-bootstrap
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Complete first-login setup for a fresh Ubuntu 24.
content_id: "5ca762774a977393"
tags: [server-setup, ubuntu, ssh, ufw, fail2ban]
---
# Server Init Bootstrap

## Summary

**One-sentence:** Complete first-login setup for a fresh Ubuntu 24.

**One-paragraph:** Complete first-login setup for a fresh Ubuntu 24.04 VPS: 5-phase sequence (access+users → system identity → packages+tools → security hardening → services foundation). Critical sequence constraint: always test SSH login as the new user BEFORE disabling root login — one wrong sshd_config line will lock you out. Requires loginctl enable-linger for systemd user services to survive logout.

## Applies If (ALL must hold)

- First login to any new VPS (Hetzner, DigitalOcean, Linode, Vultr)
- Rebuilding a server after a breach or OS reinstall
- Automating server provisioning with cloud-init user-data
- Auditing an existing server against the bootstrap checklist

## Skip If (ANY kills it)

- Managed platforms (Heroku, Railway, Render) — OS is abstracted, bootstrap doesn't apply
- Kubernetes nodes — managed by the cluster control plane, not manual setup
- Before verifying SSH key access as the new user — never disable root login first
- Running the full bootstrap on a live production server — only during initial setup

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
