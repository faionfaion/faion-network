---
slug: cloudflare-domain-dns
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: End-to-end procedure to buy a domain on Cloudflare Registrar, point it at your own server with A/AAAA records for apex+www, optional subdomain CNAMEs, decide proxy on/off per record, and lock SSL to Full(Strict).
content_id: "4347cd366d6954e4"
tags: [cloudflare, dns, registrar, domain, nameservers, ssl]
---
# Cloudflare Domain Purchase and DNS Configuration

## Summary

**One-sentence:** End-to-end procedure to buy a domain on Cloudflare Registrar, point it at your own server with A/AAAA records for apex+www, optional subdomain CNAMEs, decide proxy on/off per record, and lock SSL to Full(Strict).

**One-paragraph:** End-to-end procedure to buy a domain on Cloudflare Registrar, point it at your own server with A/AAAA records for apex+www, optional subdomain CNAMEs, decide proxy on/off per record, and lock SSL to Full(Strict). Includes propagation checks and optional API automation.

## Applies If (ALL must hold)

- Buying a brand-new domain and pointing it at your VPS or dedicated server
- Migrating an existing domain to Cloudflare Registrar after the 60-day ICANN transfer lock has expired
- Replacing the registrar's nameservers with Cloudflare's authoritative NS for an existing domain
- Adding a new server (apex + www + a few subdomains) behind Cloudflare proxy
- Centralizing DNS for multiple sites under one Cloudflare account for unified WAF and analytics

## Skip If (ANY kills it)

- Domain is locked at the current registrar (transfer lock, recent registration <60 days, or registry-lock service) — wait or unlock first
- TLD is not supported by Cloudflare Registrar (e.g. .ua, .io specialty extensions, ccTLDs requiring local presence) — keep current registrar, only delegate NS
- Domain uses DNSSEC at the parent and you cannot coordinate a DS-record swap without downtime — schedule a maintenance window or disable DNSSEC first
- You need DNS features Cloudflare does not support (e.g. DNAME chains, NAPTR for SIP, dynamic record TTL below 60s on free plan)
- Origin server has no public IPv4 and no IPv6 — DNS records would be unreachable

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
