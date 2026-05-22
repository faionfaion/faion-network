---
slug: gcp-resource-hierarchy
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP organizes all resources in a 4-level tree: Organization → Folder → Project → Resource.
content_id: "8b550f557ea2efa5"
tags: [gcp, resource-hierarchy, organization, projects, governance]
---
# GCP Resource Hierarchy Design

## Summary

**One-sentence:** GCP organizes all resources in a 4-level tree: Organization → Folder → Project → Resource.

**One-paragraph:** GCP organizes all resources in a 4-level tree: Organization → Folder → Project → Resource. IAM policies and organization constraints flow downward; projects are the billing boundary and API-enablement boundary. Designing this hierarchy upfront prevents costly restructuring later.

## Applies If (ALL must hold)

- Setting up new GCP organizations or migrating standalone projects into an organization structure.
- Designing folder and project layouts for new teams, environments, or applications.
- Planning multi-environment deployments (dev/staging/prod) with clear separation boundaries.
- Establishing governance and security foundations before teams start creating resources.

## Skip If (ANY kills it)

- Single personal project with no organizational requirements — flat project structure is sufficient.
- Read-only GCP audit tasks — hierarchy restructuring requires Organization Admin and should be done in a planned change window.

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
