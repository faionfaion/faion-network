---
slug: cicd-cert-rotation-pipeline
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Manage certificate rotation through declarative IaC: cert-manager CRDs for Kubernetes, Terraform for cloud-managed certificates (AWS ACM, GCP Certificate Manager), and Docker Compose Traefik for containerised stacks.
content_id: "6ef3236fc9394266"
tags: [tls, cert-manager, kubernetes, terraform, iac]
---
# Certificate Rotation Pipeline (cert-manager, IaC, Traefik)

## Summary

**One-sentence:** Manage certificate rotation through declarative IaC: cert-manager CRDs for Kubernetes, Terraform for cloud-managed certificates (AWS ACM, GCP Certificate Manager), and Docker Compose Traefik for containerised stacks.

**One-paragraph:** Manage certificate rotation through declarative IaC: cert-manager CRDs for Kubernetes, Terraform for cloud-managed certificates (AWS ACM, GCP Certificate Manager), and Docker Compose Traefik for containerised stacks. The canonical flow is author IaC → render TLS config → scan endpoint → diff → apply. Never commit private keys to Git — use SOPS, Vault, or External Secrets for any private material.

## Applies If (ALL must hold)

- Setting up cert-manager in Kubernetes for Ingress or Gateway API TLS termination.
- Issuing and rotating AWS ACM certificates via Terraform with Route53 DNS validation.
- Configuring Docker Compose Traefik as an ACME-based reverse proxy with auto-renewal.
- Implementing rotation policy: privateKey.rotationPolicy: Always so certs rotate on renewal, not just replacement.
- Any pipeline that provisions or re-provisions infrastructure and needs certs issued automatically as part of the IaC apply step.

## Skip If (ANY kills it)

- Bare-metal servers without Kubernetes — use certbot/acme.sh directly (see cicd-tls-renewal-automation).
- Service-mesh mTLS — Linkerd/Istio/Cilium auto-rotate identities; do not layer cert-manager on top of a mesh's identity plane.
- App-layer encryption (envelope encryption of payloads, JWE) — different methodology entirely.
- Short-lived internal certs where Vault PKI or step-ca is the issuer — those have their own rotation APIs.

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
