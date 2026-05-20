---
slug: gitops-secrets-security
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Secrets in GitOps require explicit tooling because plaintext secrets in Git are a critical vulnerability.
content_id: "8ae3e1e1105f3ac0"
tags: [gitops, secrets, sops, security, kubernetes]
---
# GitOps Secret Management and Security

## Summary

**One-sentence:** Secrets in GitOps require explicit tooling because plaintext secrets in Git are a critical vulnerability.

**One-paragraph:** Secrets in GitOps require explicit tooling because plaintext secrets in Git are a critical vulnerability. Three mature solutions exist: SOPS (encrypt-in-place, Git-native), Sealed Secrets (cluster-encrypted CRDs), and External Secrets Operator (pull from Vault/AWS SM/GCP SM). Each has distinct trust models. Security hardening covers RBAC, network policies, and AI-agent-specific risks.

## Applies If (ALL must hold)

- Any GitOps setup — secret management is mandatory, not optional.
- SOPS: when the team controls key management (age keys, AWS KMS, GCP KMS) and wants secrets to live in Git in encrypted form.
- Sealed Secrets: when secrets should be cluster-scoped and you want a simple CLI (kubeseal) without external KMS dependency.
- External Secrets Operator: when secrets already live in Vault, AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault and you want to avoid duplicating them.

## Skip If (ANY kills it)

- Sealed Secrets: do not use across multiple clusters without managing cluster-specific keys — a sealed secret from cluster A cannot be decrypted by cluster B.
- SOPS with shared age keys: avoid single shared key for all environments — use per-environment keys so staging keys cannot decrypt prod secrets.
- External Secrets without network policy: ESO requires egress from the cluster to the secret store — ensure network policies allow this only from the ESO namespace.

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
