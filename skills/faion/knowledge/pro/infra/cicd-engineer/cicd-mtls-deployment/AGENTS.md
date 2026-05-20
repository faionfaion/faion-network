---
slug: cicd-mtls-deployment
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure mutual TLS for service-to-service authentication: nginx ssl_client_certificate verification, internal CA setup with step-ca or Vault PKI, client certificate issuance and rotation, and mTLS testing via curl.
content_id: "ac3e2239574fd8a9"
tags: [mtls, tls, service-mesh, internal-ca, zero-trust]
---
# Mutual TLS (mTLS) Deployment in CI/CD Pipelines

## Summary

**One-sentence:** Configure mutual TLS for service-to-service authentication: nginx ssl_client_certificate verification, internal CA setup with step-ca or Vault PKI, client certificate issuance and rotation, and mTLS testing via curl.

**One-paragraph:** Configure mutual TLS for service-to-service authentication: nginx ssl_client_certificate verification, internal CA setup with step-ca or Vault PKI, client certificate issuance and rotation, and mTLS testing via curl. For K8s service mesh, delegate mTLS to the mesh (Linkerd/Istio/Cilium) and do not hand-roll — short-lived per-pod identity certs are the de-facto standard.

## Applies If (ALL must hold)

- Service-to-service authentication for internal APIs where network-layer identity is required (zero-trust architecture).
- Setting up an internal CA (step-ca or Vault PKI) for automated short-lived cert issuance to services.
- Configuring nginx or HAProxy as an mTLS termination point that forwards client identity headers to the backend.
- Issuing client certificates programmatically from CI/CD pipelines for service-to-service auth in staging or production.
- Migration from shared long-lived client certs to short-lived per-service certs.

## Skip If (ANY kills it)

- Kubernetes service mesh environments — Linkerd, Istio, and Cilium auto-rotate per-pod mTLS identities; do not hand-roll on top of a mesh's identity plane.
- App-layer encryption (JWE, envelope encryption) — different methodology; mTLS only secures the transport layer.
- Public-facing client authentication — mTLS with browser clients requires distributing client certs to end users, which is rarely practical.
- VPN/IPSec — different protocols and CA structures apply.

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
