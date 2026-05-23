---
slug: external-secrets-operator-recipe
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Production-ready ESO setup recipe: ClusterSecretStore configuration per backend, ExternalSecret manifests, refresh interval calibration, RBAC, secret-store identity, alerts on sync failure."
content_id: "4becbeb92163400f"
complexity: medium
produces: config
est_tokens: 3900
tags: [infra, pro, runbook, eso, kubernetes, secrets]
---

# External Secrets Operator Recipe

## Summary

**One-sentence:** Production-ready ESO setup recipe: ClusterSecretStore configuration per backend, ExternalSecret manifests, refresh interval calibration, RBAC, secret-store identity, alerts on sync failure.

**One-paragraph:** External Secrets Operator (ESO) is the modern Kubernetes secrets-injection standard. Setup is straightforward; production hardening is where teams trip: refresh interval too aggressive (rate-limiting), no alerts on sync failure (silent staleness), wide RBAC (any pod can read any secret), no rotation propagation (rotated backend secret not picked up). This recipe pins the configuration: ClusterSecretStore per backend with identity-based auth (IRSA / Workload Identity), ExternalSecret per service with refresh interval calibrated to backend rate limits, RBAC scoped to namespace, alerts on sync failures, rotation-test runbook.

**Ефективно для:**

- ClusterSecretStore + ExternalSecret замість kubectl create secret.
- Identity-based auth (IRSA / Workload Identity) — без static keys.
- Refresh interval calibrated до backend rate limits.
- Alert на sync failure — silent staleness detected.

## Applies If (ALL must hold)

- Kubernetes cluster (>=1.24)
- Secrets backend in place (Vault / AWS Secrets Manager / GCP Secret Manager / Azure KeyVault)
- Cloud identity available (IRSA / Workload Identity / OIDC)
- Need to inject secrets into pods without manual kubectl

## Skip If (ANY kills it)

- Vendor-managed K8s with pre-installed secrets injection (use vendor's)
- Single-pod single-secret workload — ESO overhead exceeds value

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes cluster admin | kubeconfig | platform team |
| Secrets backend with identity-based auth | backend URL + role/policy | platform team |
| Helm + Flux/Argo for ESO install | GitOps repo | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[secrets-management]] | Backend choice + identity strategy |
| [[security-as-code]] | RBAC + admission control |

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
| `css_manifest_draft` | sonnet | Backend-specific manifest synthesis |
| `external_secret_per_service` | haiku | Template fill |
| `rotation_test_script` | sonnet | Bash + kubectl orchestration |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-external-secrets-operator-recipe.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[secrets-management]]
- [[security-as-code]]
- [[ssl-tls-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
