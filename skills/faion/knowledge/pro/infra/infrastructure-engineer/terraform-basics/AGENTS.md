---
slug: terraform-basics
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core Terraform reference covering HCL syntax, provider configuration, resources, data sources, variables, outputs, locals, and the standard project file layout.
content_id: "a719bf81abe7f546"
tags: [[]]
---
# Terraform Basics

## Summary

**One-sentence:** Core Terraform reference covering HCL syntax, provider configuration, resources, data sources, variables, outputs, locals, and the standard project file layout.

**One-paragraph:** Core Terraform reference covering HCL syntax, provider configuration, resources, data sources, variables, outputs, locals, and the standard project file layout. The concrete rule: always use for_each over count when resources need unique identifiers; always store state remotely with locking enabled; never commit *.tfstate* or actual terraform.tfvars files.

## Applies If (ALL must hold)

- Starting a new Terraform project and scaffolding the file structure
- Configuring providers (AWS, GCP, Azure) with version constraints and default tags
- Writing resources with proper meta-arguments (count, for_each, lifecycle, depends_on)
- Looking up built-in function syntax (string, collection, encoding, date functions)
- Setting up remote state backends (S3+DynamoDB, GCS, Azure Blob, Terraform Cloud)

## Skip If (ANY kills it)

- Advanced state operations (import, mv, rm, moved blocks) — use terraform-state methodology
- Production CI/CD pipeline patterns — use the advanced terraform methodology
- Module design and versioning — use terraform-modules methodology
- AWS/GCP-specific resource patterns — use the respective cloud methodology

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
