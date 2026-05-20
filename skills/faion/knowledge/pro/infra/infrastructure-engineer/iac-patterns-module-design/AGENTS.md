---
slug: iac-patterns-module-design
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Five canonical Terraform module patterns (Base, Wrapper, Facade, Factory, Composite) that cover the full design space from single-resource encapsulation to simplified stack facades.
content_id: "e4055b9edd541a3d"
tags: [terraform, iac, modules, infrastructure, opentofu]
---
# IaC Module Design Patterns

## Summary

**One-sentence:** Five canonical Terraform module patterns (Base, Wrapper, Facade, Factory, Composite) that cover the full design space from single-resource encapsulation to simplified stack facades.

**One-paragraph:** Five canonical Terraform module patterns (Base, Wrapper, Facade, Factory, Composite) that cover the full design space from single-resource encapsulation to simplified stack facades. Each pattern has a specific use case; mixing them correctly is the key skill.

## Applies If (ALL must hold)

- Creating a new reusable module — choose the pattern before writing any HCL.
- Refactoring copy-pasted resource blocks into a shared module.
- Enforcing organization security/compliance defaults across teams (Wrapper pattern).
- Exposing a simplified API for complex multi-resource deployments (Facade pattern).
- Creating identical resources from a configuration map (Factory pattern).

## Skip If (ANY kills it)

- One-off environment root modules — patterns add overhead without reuse benefit.
- Prototype or throwaway stacks — apply patterns only to modules intended for reuse.
- When the resource already has a community module that meets requirements — wrap, don't recreate.

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
