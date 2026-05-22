---
slug: cicd-tls-renewal-automation
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Automate certificate renewal end-to-end: ACME client selection, systemd timer or cron scheduling, post-renew reload hooks, and short-lived cert policy.
content_id: "3d4d238d18c2881d"
tags: [tls, certificates, acme, automation, let-s-encrypt]
---
# TLS Certificate Renewal Automation

## Summary

**One-sentence:** Automate certificate renewal end-to-end: ACME client selection, systemd timer or cron scheduling, post-renew reload hooks, and short-lived cert policy.

**One-paragraph:** Automate certificate renewal end-to-end: ACME client selection, systemd timer or cron scheduling, post-renew reload hooks, and short-lived cert policy. Manual renewal is an outage waiting to happen — treat it as a reliability requirement.

## Applies If (ALL must hold)

- Issuing and rotating certificates for public web or API endpoints (Let's Encrypt, ZeroSSL, commercial CA).
- Adopting short-lived certs (LE 6-day or 45-day) where manual renewal is structurally impossible.
- Setting up post-renewal hooks to reload nginx/apache/traefik after certificate update.
- Configuring ACME Renewal Information (ARI) checks to catch early renewal recommendations from the CA.
- Any CI/CD pipeline that provisions or re-provisions infrastructure and needs certs issued automatically.

## Skip If (ANY kills it)

- Internal-only dev environments where mkcert self-signed is sufficient and not regulated — overhead exceeds value.
- Service-mesh mTLS — Linkerd/Istio/Cilium auto-rotate identities; do not hand-roll ACME on top of a mesh.
- Legacy systems mandated to use TLS 1.0/1.1 — you have a compliance/risk problem, not a setup problem.
- VPN/IPSec — different protocols and certificate authorities apply.

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

- parent skill: `pro/infra/cicd-engineer/`
