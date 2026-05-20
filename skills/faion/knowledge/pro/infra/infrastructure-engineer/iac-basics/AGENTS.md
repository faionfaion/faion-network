---
slug: iac-basics
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Infrastructure as Code applies software engineering practices to infrastructure management through declarative or imperative code definitions.
content_id: "f9269dc7ba7bc8d5"
tags: [infrastructure-as-code, terraform, gitops, iac, pulumi]
---
# Infrastructure as Code (IaC) Fundamentals

## Summary

**One-sentence:** Infrastructure as Code applies software engineering practices to infrastructure management through declarative or imperative code definitions.

**One-paragraph:** Infrastructure as Code applies software engineering practices to infrastructure management through declarative or imperative code definitions. This enables version control, testing, automation, and consistency across environments. IaC market projected to reach USD 6.14 billion by 2033, growing at 22%+ CAGR (2025-2033).

## Applies If (ALL must hold)

- Provisioning cloud infrastructure (VPCs, clusters, databases, storage) that will change over time and must remain consistent across environments.
- Team environments where multiple engineers apply infrastructure changes and concurrent access must be serialized via state locking.
- Compliance and audit requirements that mandate a full change history for infrastructure modifications.
- Disaster recovery scenarios where an entire environment must be reproducible from code.
- Multi-environment setups (dev/staging/prod) where parity between environments is critical.
- GitOps workflows where infrastructure changes are triggered by PR merges, not ad-hoc CLI commands.

## Skip If (ANY kills it)

- Throwaway personal experiments where overhead exceeds value — use cloud console or CLI directly.
- Pure configuration management on existing machines — use Ansible or Chef rather than Terraform.
- Kubernetes resource management inside an existing cluster — use Helm/Kustomize rather than Terraform for K8s objects.

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
