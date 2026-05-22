---
slug: devops-platform-crossplane
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Crossplane extends Kubernetes with Composite Resource Definitions (XRDs) so platform teams define infrastructure abstractions (Database, Cache, Network) as custom CRDs.
content_id: "647e284fa74eb98a"
tags: [crossplane, kubernetes, infrastructure-as-code, platform-engineering, cncf]
---
# Crossplane: Kubernetes-Native Infrastructure Compositions

## Summary

**One-sentence:** Crossplane extends Kubernetes with Composite Resource Definitions (XRDs) so platform teams define infrastructure abstractions (Database, Cache, Network) as custom CRDs.

**One-paragraph:** Crossplane extends Kubernetes with Composite Resource Definitions (XRDs) so platform teams define infrastructure abstractions (Database, Cache, Network) as custom CRDs. Developers submit simple claim objects; Crossplane reconciles the full multi-resource stack with security defaults embedded. This gives developers a self-service API surface while platform teams retain control over security, cost, and compliance through the composition layer.

## Applies If (ALL must hold)

- Platform team building self-service infrastructure abstractions on top of AWS, GCP, or Azure.
- Orgs already using Kubernetes who want infrastructure provisioning to follow the same GitOps workflow as application deployments.
- Multi-cloud environments where the same developer-facing API (e.g., Database claim) must provision to different cloud backends depending on environment.
- Infrastructure that needs continuous reconciliation (drift correction) rather than one-time apply.

## Skip If (ANY kills it)

- Teams not running Kubernetes — Crossplane requires a Kubernetes cluster as its control plane; the overhead is not justified without an existing cluster.
- Simple single-resource provisioning where a Terraform module achieves the same result with less operational complexity.
- Orgs without Kubernetes expertise — Crossplane debugging requires understanding Kubernetes reconciliation loops and CRD status conditions.

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
