---
slug: cloudflare-domain-dns
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "End-to-end procedure to buy a domain on Cloudflare Registrar, point it at your own server (A/AAAA + CNAMEs), choose proxy per record, lock SSL to Full(Strict), and verify propagation from multiple resolvers."
content_id: "4347cd366d6954e4"
complexity: medium
produces: report
est_tokens: 6000
tags: [cloudflare, dns, registrar, domain, ssl]
---
# Cloudflare Domain + DNS

## Summary

**One-sentence:** End-to-end procedure to buy a domain on Cloudflare Registrar, point it at your own server (A/AAAA + CNAMEs), choose proxy per record, lock SSL to Full(Strict), and verify propagation from multiple resolvers.

**One-paragraph:** Cloudflare Registrar sells domains at wholesale registry cost and routing DNS through Cloudflare gives free DDoS, edge cache, and a 15-year origin certificate that ends the 90-day Let's Encrypt renewal cycle. Configuring it correctly avoids two classic outages: Flexible-SSL redirect loops and AAAA records left dangling on dual-stack origins. This methodology produces a verified DNS plan with proxy decisions documented per record + propagation evidence from external resolvers.

## Applies If (ALL must hold)

- Buying a new domain or migrating to Cloudflare Registrar after 60-day lock.
- Adding a new server (apex + www + subdomains) behind Cloudflare proxy.
- Centralizing DNS for multiple sites in one Cloudflare account.

## Skip If (ANY kills it)

- Domain is in registry/transfer lock — wait or unlock first.
- TLD not supported by Cloudflare Registrar (e.g. .ua, niche ccTLDs).
- Origin has no public IPv4 and no IPv6 — records would be unreachable.

**Ефективно для:**

- Indie-проєкти що купують перший домен — рідний шлях для self-hosted.
- Перенесення з GoDaddy / Namecheap — економія 30-50% на renewal.
- Setups з кількох сайтів під одним dashboard.
- Стабільний 15-річний origin cert замість 90-day LE-renewals.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/ssl-tls-management` | Origin cert installation steps. |
| `solo/infra/server-craft/nginx-reverse-proxy` | Server-side TLS termination. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown DNS plan with per-record proxy justification. |
| `templates/_smoke-test.md` | Minimum viable filled-in DNS plan. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloudflare-domain-dns.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[ssl-tls-management]]
- [[nginx-reverse-proxy]]
- [[cloudflare-pages-github]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
