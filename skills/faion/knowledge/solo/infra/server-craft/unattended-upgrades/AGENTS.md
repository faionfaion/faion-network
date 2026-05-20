---
slug: unattended-upgrades
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Automate security patch management on Ubuntu 24.
content_id: "ce0e8289fedb01e3"
tags: [ubuntu, security, automation, patching, infrastructure]
---
# Unattended Upgrades

## Summary

**One-sentence:** Automate security patch management on Ubuntu 24.

**One-paragraph:** Automate security patch management on Ubuntu 24.04 with `unattended-upgrades`: enable daily security-origin updates, schedule auto-reboot at off-peak hours (4 AM), blacklist packages that require manual intervention (Docker, databases), and clean up old kernels automatically. Services must have `Restart=always` and Docker containers `restart: unless-stopped` to recover after automatic reboots.

## Applies If (ALL must hold)

- Any production Ubuntu VPS that should stay patched without manual intervention
- Servers running kernel-level services where CVEs appear frequently (OpenSSL, libc, systemd)
- Configuring auto-reboot after kernel updates to apply them
- Auditing whether existing auto-update config is correct

## Skip If (ANY kills it)

- During initial server setup before verifying all services have `Restart=always` — auto-reboot will leave services down
- For database major version upgrades — blacklist the package and upgrade manually after testing
- When using a managed platform that handles patching (Heroku, Railway) — don't install unattended-upgrades there
- For Docker CE — version changes can break container runtimes; always blacklist and upgrade manually

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
