---
slug: secrets-management
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Secrets management spec: eliminate static credentials, use cloud identity (IRSA / Workload Identity / OIDC), short-lived dynamic credentials, 30-day rotation, ESO for Kubernetes injection."
content_id: "5646b8f8e846e9ab"
complexity: medium
produces: config
est_tokens: 3900
tags: [secrets, vault, kubernetes, oidc, eso]
---

# Secrets Management

## Summary

**One-sentence:** Secrets management spec: eliminate static credentials, use cloud identity (IRSA / Workload Identity / OIDC), short-lived dynamic credentials, 30-day rotation, ESO for Kubernetes injection.

**One-paragraph:** Secrets management in 2025-2026 means eliminating static, long-lived credentials. Apps authenticate via cloud identity (IRSA on EKS, Workload Identity on GKE, OIDC for CI/CD) and receive short-lived dynamic credentials from a secrets backend (Vault, AWS Secrets Manager, GCP Secret Manager). Kubernetes integration uses External Secrets Operator (ESO) as the bridge. Rotation is automated on a 30-day or shorter cycle. Static keys in env vars, repo files, or CI variables are the primary breach vector and must be eradicated.

**Ефективно для:**

- Eliminate static AWS/GCP/Vault keys в CI/CD через OIDC trust.
- Kubernetes pod secrets через ESO замість kubectl create secret.
- Automated rotation на 30-денному циклі без app downtime.
- Audit trail для secret access (хто, коли, який secret).

## Applies If (ALL must hold)

- Application needs database credentials, API keys, or TLS certificates at runtime
- Kubernetes workloads require secrets without storing them as native K8s Secrets in plain base64
- CI/CD pipelines must authenticate to cloud providers without stored access keys
- Compliance requires secret rotation, audit logging, and access control (SOC2, HIPAA, PCI-DSS)

## Skip If (ANY kills it)

- Development-only local environment — .env files are acceptable
- Secrets that are truly public (public API keys, non-sensitive config) — use ConfigMaps
- Single-cloud project where cloud-native secrets service covers all use cases — Vault is unnecessary overhead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud account with identity provider (AWS IAM / GCP IAM / Azure AD) | IAM policies | platform team |
| Secrets backend (Vault / AWS Secrets Manager / GCP Secret Manager) | credentials + backend URL | platform team |
| Kubernetes cluster (for ESO use case) | kubeconfig + namespace | platform team |
| GitHub / GitLab project (for OIDC CI/CD) | repo settings + admin rights | DevOps lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[external-secrets-operator-recipe]] | ESO setup pattern for Kubernetes injection |
| [[ssl-tls-setup]] | TLS for secrets-in-transit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_secrets` | haiku | Listing existing credentials is mechanical |
| `policy_design` | sonnet | Least-privilege policy synthesis |
| `backend_choice` | opus | Cross-cloud + compliance tradeoff judgment |

## Templates

| File | Purpose |
|------|---------|
| `templates/eso-secret-store.yaml` | Eso secret store template |
| `templates/prompt-audit.txt` | Prompt audit template |
| `templates/vault-policy.hcl` | Vault policy template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-secrets-management.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[external-secrets-operator-recipe]]
- [[ssl-tls-setup]]
- [[security-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
