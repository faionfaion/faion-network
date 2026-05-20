---
slug: vector-db-security
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Harden a vector database deployment against unauthorized access and data leakage: disable anonymous access, configure API key or OIDC authentication, enforce TLS for all connections, deploy in a private VPC subnet, enable encryption at rest, set up audit logging, and define PII handling procedures.
content_id: "a0d0baa91763cc20"
tags: [vector-database, security, authentication, tls, network-isolation]
---
# Vector Database Security Hardening

## Summary

**One-sentence:** Harden a vector database deployment against unauthorized access and data leakage: disable anonymous access, configure API key or OIDC authentication, enforce TLS for all connections, deploy in a private VPC subnet, enable encryption at rest, set up audit logging, and define PII handling procedures.

**One-paragraph:** Harden a vector database deployment against unauthorized access and data leakage: disable anonymous access, configure API key or OIDC authentication, enforce TLS for all connections, deploy in a private VPC subnet, enable encryption at rest, set up audit logging, and define PII handling procedures.

## Applies If (ALL must hold)

- Any vector database deployment that handles non-public data (user documents, internal knowledge bases, PII-adjacent text).
- Before promoting a development deployment to production traffic.
- When adding a vector database to a stack that already enforces network isolation for other services.
- Compliance requirements (SOC2, GDPR, HIPAA) mandate audit logging and encryption.

## Skip If (ANY kills it)

- Local development with only synthetic data — anonymous access is acceptable to minimize setup friction.
- Fully managed services (Pinecone Serverless, Weaviate Cloud) — authentication and network security are managed by the provider; verify their compliance docs instead.

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

- parent skill: `geek/ai/ml-engineer/`
