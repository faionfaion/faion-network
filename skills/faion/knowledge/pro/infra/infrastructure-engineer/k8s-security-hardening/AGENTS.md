---
slug: k8s-security-hardening
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes workload security requires five layers: Pod Security Standards (enforce restricted namespace labels), container securityContext (non-root, read-only root filesystem, drop ALL capabilities), dedicated ServiceAccounts with minimal RBAC, NetworkPolicies enforcing default-deny with explicit allow rules, and secrets never stored in ConfigMaps or environment variables — use secretKeyRef or an external vault.
content_id: "80512dc55d963c5b"
tags: [kubernetes, security, pod-security-standards, networkpolicy, rbac]
---
# Kubernetes Security Hardening

## Summary

**One-sentence:** Kubernetes workload security requires five layers: Pod Security Standards (enforce restricted namespace labels), container securityContext (non-root, read-only root filesystem, drop ALL capabilities), dedicated ServiceAccounts with minimal RBAC, NetworkPolicies enforcing default-deny with explicit allow rules, and secrets never stored in ConfigMaps or environment variables — use secretKeyRef or an external vault.

**One-paragraph:** Kubernetes workload security requires five layers: Pod Security Standards (enforce restricted namespace labels), container securityContext (non-root, read-only root filesystem, drop ALL capabilities), dedicated ServiceAccounts with minimal RBAC, NetworkPolicies enforcing default-deny with explicit allow rules, and secrets never stored in ConfigMaps or environment variables — use secretKeyRef or an external vault.

## Applies If (ALL must hold)

- Deploying any production workload to Kubernetes.
- Auditing an existing Deployment for security misconfigurations.
- Setting up a new namespace for production workloads.
- Implementing zero-trust pod-to-pod communication.
- Reviewing secrets management practices.

## Skip If (ANY kills it)

- Development namespaces with throwaway workloads where security overhead slows iteration — use baseline PSS at minimum.
- Legacy applications that genuinely require root (e.g., some database init scripts) — use securityContext.runAsUser: 0 explicitly rather than omitting it, and document the exception.
- Namespace-level PSS enforcement on namespaces with existing workloads before validating compatibility — start with warn mode.

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
