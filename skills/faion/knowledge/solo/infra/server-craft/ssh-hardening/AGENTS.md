---
slug: ssh-hardening
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenSSH server hardening for Ubuntu/Debian VPS: key-only authentication (ed25519), drop-in config via `sshd_config.
content_id: "73eaf324b3be62b7"
tags: [ssh, security, ubuntu, hardening, systemd]
---
# SSH Hardening

## Summary

**One-sentence:** OpenSSH server hardening for Ubuntu/Debian VPS: key-only authentication (ed25519), drop-in config via `sshd_config.

**One-paragraph:** OpenSSH server hardening for Ubuntu/Debian VPS: key-only authentication (ed25519), drop-in config via `sshd_config.d/`, modern crypto (curve25519 KEX + AEAD ciphers), port change via systemd socket override, and client `~/.ssh/config` with connection multiplexing. The critical safety rule is: always keep a second terminal session open and test the new connection BEFORE closing the original session.

## Applies If (ALL must hold)

- Bootstrapping a new VPS — SSH hardening is required before any other service is exposed
- After adding a new user who needs SSH access — `AllowUsers` must be updated
- Auditing an existing server's SSH config against Mozilla SSH guidelines
- Rotating SSH keys (compromised key, new machine)
- Configuring SSH client for multi-server workflows with ProxyJump

## Skip If (ANY kills it)

- Servers already behind Tailscale/WireGuard where SSH is not reachable from the public internet (still good practice, but urgency is lower)
- Ephemeral containers or CI runners — hardening overhead not worth it for short-lived instances
- Servers with a vetted existing config — re-running risks lockout if the second-terminal test sequence is skipped

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
