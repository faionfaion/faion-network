---
slug: ssl-tls-setup
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications.
content_id: "8a08a611be49cb7c"
tags: [ssl, tls, certificates, lets-encrypt, cert-manager]
---
# SSL/TLS Setup

## Summary

**One-sentence:** SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications.

**One-paragraph:** SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications. This methodology covers certificate management, configuration best practices, and implementation across various platforms.

## Applies If (ALL must hold)

- Securing web applications with HTTPS
- Protecting API communications
- Implementing mutual TLS (mTLS) for service-to-service auth
- Meeting compliance requirements (PCI-DSS, HIPAA)
- Securing internal services
- Kubernetes ingress TLS termination

## Skip If (ANY kills it)

- Internal loopback-only services that never leave the process boundary — TLS overhead is unnecessary
- Development environments using localhost only — self-signed certs are acceptable without full HSTS/OCSP setup
- Air-gapped systems where certificate renewal automation is impossible and manual rotation cadence is controlled

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

- parent skill: `pro/infra/devops-engineer/`
