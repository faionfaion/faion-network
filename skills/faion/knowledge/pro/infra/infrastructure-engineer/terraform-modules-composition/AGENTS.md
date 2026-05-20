---
slug: terraform-modules-composition
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Module composition is how root modules assemble child modules into a complete infrastructure system.
content_id: "eaf1e5b9913c0ab5"
tags: [terraform, modules, composition, patterns, iac]
---
# Terraform Module Composition Patterns

## Summary

**One-sentence:** Module composition is how root modules assemble child modules into a complete infrastructure system.

**One-paragraph:** Module composition is how root modules assemble child modules into a complete infrastructure system. Three patterns cover most use cases: flat composition for simple architectures, hierarchical composition for layered abstraction, and the factory pattern using for_each for dynamic multi-instance provisioning. DRY techniques (locals, environment config maps) reduce duplication across callers.

## Applies If (ALL must hold)

- Assembling a root module from multiple child modules (VPC + ECS + RDS).
- Deploying multiple nearly-identical instances of the same module (microservices, per-team environments).
- Applying the same module call across dev/staging/prod with different variable values.
- Reducing copy-paste of tag maps and environment configs across module calls.

## Skip If (ANY kills it)

- Single-resource modules — composition overhead exceeds value for modules with one or two resources.
- When modules have circular dependencies — Terraform does not support cycles; restructure the module graph first.

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
