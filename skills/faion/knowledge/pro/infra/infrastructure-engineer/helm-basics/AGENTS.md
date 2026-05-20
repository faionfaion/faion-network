---
slug: helm-basics
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Helm is the package manager for Kubernetes, enabling templating, versioning, and sharing of Kubernetes manifests.
content_id: "2aa1ae92281f3edd"
tags: [helm, kubernetes, package-manager, templating, gitops]
---
# Helm Basics

## Summary

**One-sentence:** Helm is the package manager for Kubernetes, enabling templating, versioning, and sharing of Kubernetes manifests.

**One-paragraph:** Helm is the package manager for Kubernetes, enabling templating, versioning, and sharing of Kubernetes manifests. Charts bundle related resources into reusable, configurable packages with dependency management and release lifecycle control. Master chart structure (Chart.yaml, values.yaml, templates/), template syntax, and release management commands (install, upgrade, rollback) to deploy applications consistently across environments.

## Applies If (ALL must hold)

- Deploying complex applications with many Kubernetes resources (Deployment, Service, Ingress, ConfigMap, Secret, HPA, PDB).
- Managing multiple environments (dev, staging, prod) with different configurations without duplicating manifests.
- Creating reusable deployment packages for internal team use or public distribution.
- Implementing GitOps workflows where Helm releases are defined in Git and synced by controllers (ArgoCD, Flux).
- Standardizing Kubernetes deployments across organization to enforce naming conventions, labels, and security policies.
- Sharing applications across teams or organizations (e.g., publishing to Artifact Hub or private registries).

## Skip If (ANY kills it)

- Single-manifest deployments (one Deployment, one Service) — raw kubectl apply is simpler and adds no overhead.
- Highly dynamic manifests requiring logic beyond simple templating — use Kustomize or custom controllers for complex transformations.
- Secrets management — Helm templates should not store encrypted secrets; use external secret managers (Sealed Secrets, Vault, AWS Secrets Manager) with templated references.
- Cluster provisioning (cluster creation, node pools, RBAC setup) — use Terraform or cloud-specific tools; Helm manages applications post-provisioning.

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

- parent skill: `pro/infra/infrastructure-engineer/`
