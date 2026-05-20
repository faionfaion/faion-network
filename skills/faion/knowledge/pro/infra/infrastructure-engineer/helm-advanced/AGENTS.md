---
slug: helm-advanced
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced Helm techniques for production-grade chart development: library charts for reusable templates, hooks for lifecycle intervention (pre-install, post-upgrade, test), Helm test framework for deployment validation, umbrella charts for multi-service composition, and production patterns (checksum annotations, required values, resource protection).
content_id: "e848dff2800dcf0f"
tags: [helm, kubernetes, library-charts, hooks, testing, umbrella-charts]
---
# Helm Advanced Patterns

## Summary

**One-sentence:** Advanced Helm techniques for production-grade chart development: library charts for reusable templates, hooks for lifecycle intervention (pre-install, post-upgrade, test), Helm test framework for deployment validation, umbrella charts for multi-service composition, and production patterns (checksum annotations, required values, resource protection).

**One-paragraph:** Advanced Helm techniques for production-grade chart development: library charts for reusable templates, hooks for lifecycle intervention (pre-install, post-upgrade, test), Helm test framework for deployment validation, umbrella charts for multi-service composition, and production patterns (checksum annotations, required values, resource protection). Master these patterns to build maintainable, testable charts at enterprise scale.

## Applies If (ALL must hold)

- Creating library charts to share template logic (naming, labels, common patterns) across 5+ application charts to reduce duplication.
- Implementing lifecycle hooks for database migrations (pre-upgrade), smoke tests (post-install), or cleanup (pre-delete).
- Validating deployed releases with Helm tests that confirm connectivity, health checks, and basic functionality.
- Composing multi-service applications (app + PostgreSQL + Redis) with coordinated deployments using umbrella charts.
- Enforcing production practices: config checksums, required values validation, resource protection, Helm linting in CI/CD.

## Skip If (ANY kills it)

- Simple single-service deployments — basic Helm covers this; library charts add overhead without benefit.
- Lifecycle operations requiring external systems (Kubernetes operators, custom controllers) — hooks are limited to Kubernetes Jobs/Pods.
- Complex multi-service orchestration with inter-service coordination — use Kubernetes operators or GitOps controllers (ArgoCD, Flux) for advanced scenarios.
- Services with independent release cycles that need to be deployed separately — avoid umbrella charts; manage at GitOps level instead.

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
