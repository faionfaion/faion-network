---
slug: devops-lb-ssl-tls
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The load balancer can terminate TLS (decrypt and forward HTTP to backends), re-encrypt (decrypt and re-encrypt to backends), or pass through (forward encrypted traffic unchanged).
content_id: "7d9526b3572d7c37"
tags: [ssl, tls, load-balancing, security, certificates]
---
# SSL/TLS Termination at the Load Balancer

## Summary

**One-sentence:** The load balancer can terminate TLS (decrypt and forward HTTP to backends), re-encrypt (decrypt and re-encrypt to backends), or pass through (forward encrypted traffic unchanged).

**One-paragraph:** The load balancer can terminate TLS (decrypt and forward HTTP to backends), re-encrypt (decrypt and re-encrypt to backends), or pass through (forward encrypted traffic unchanged). Termination is the standard choice; it offloads CPU and enables L7 routing. TLS 1.3 is preferred; TLS 1.2 is the minimum acceptable in 2025-2026.

## Applies If (ALL must hold)

- Any public-facing HTTP service — TLS termination at the LB is the standard production pattern.
- Environments that require end-to-end encryption (re-encryption) for compliance (PCI-DSS, HIPAA).
- Services using gRPC or WebSocket over TLS where header inspection is not needed (passthrough).
- Multi-domain services where one LB must serve multiple certificates (SNI-based routing).

## Skip If (ANY kills it)

- Passthrough mode disables all L7 routing — do not use it if path-based or host-based routing is required.
- Do not terminate TLS on a load balancer that does not hold the private key securely (use HSM or vault-injected secrets).

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
