---
slug: wireguard-vpn
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure WireGuard as a VPN server on a Linux VPS with multiple peer types: split-tunnel dev machine (VPN subnet only), full-tunnel mobile (all traffic), and site-to-site gateway (VPS to home LAN).
content_id: "1c513aa80a1db2a1"
tags: [wireguard, vpn, networking, security, linux]
---
# WireGuard VPN

## Summary

**One-sentence:** Configure WireGuard as a VPN server on a Linux VPS with multiple peer types: split-tunnel dev machine (VPN subnet only), full-tunnel mobile (all traffic), and site-to-site gateway (VPS to home LAN).

**One-paragraph:** Configure WireGuard as a VPN server on a Linux VPS with multiple peer types: split-tunnel dev machine (VPN subnet only), full-tunnel mobile (all traffic), and site-to-site gateway (VPS to home LAN). Uses cryptokey routing — each peer's AllowedIPs list determines which packets are routed to it.

## Applies If (ALL must hold)

- Accessing internal VPS services (PostgreSQL, Redis, RabbitMQ) securely without exposing ports to the internet
- Creating a site-to-site tunnel between a VPS and home network/Raspberry Pi
- Routing all mobile traffic through the VPS for privacy on public Wi-Fi
- Restricting SSH access to VPN subnet only (after VPN is confirmed working)

## Skip If (ANY kills it)

- When you only need SSH access — an SSH tunnel (`ssh -L`) is simpler and requires no server-side setup
- When your provider already offers a managed VPN or private networking between servers — use that instead
- As a replacement for UFW — WireGuard controls which hosts can connect; UFW controls which ports are exposed. Both are needed

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
