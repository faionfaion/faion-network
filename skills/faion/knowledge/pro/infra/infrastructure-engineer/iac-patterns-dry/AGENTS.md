---
slug: iac-patterns-dry
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four DRY techniques for Terraform that eliminate duplication without sacrificing readability: locals for computed/derived values, for_each (not count) for similar resources, dynamic blocks for repeated nested structures, and Terragrunt for eliminating provider/backend boilerplate across environments.
content_id: "496677357c58530e"
tags: [terraform, iac, dry, terragrunt, refactoring]
---
# IaC DRY Patterns

## Summary

**One-sentence:** Four DRY techniques for Terraform that eliminate duplication without sacrificing readability: locals for computed/derived values, for_each (not count) for similar resources, dynamic blocks for repeated nested structures, and Terragrunt for eliminating provider/backend boilerplate across environments.

**One-paragraph:** Four DRY techniques for Terraform that eliminate duplication without sacrificing readability: locals for computed/derived values, for_each (not count) for similar resources, dynamic blocks for repeated nested structures, and Terragrunt for eliminating provider/backend boilerplate across environments.

## Applies If (ALL must hold)

- Three or more identical resource blocks differing only in name/tags — use for_each with a map.
- Repeated nested blocks (ingress rules, lifecycle rules, tag sets) — use dynamic blocks.
- Values derived from input variables repeated in multiple expressions — use locals.
- Multiple Terraform environments sharing the same provider/backend config — use Terragrunt.
- Refactoring review: scanning for copy-pasted patterns before a module extraction.

## Skip If (ANY kills it)

- Single-resource modules — DRY adds abstraction overhead with no benefit when there's nothing to deduplicate.
- for_each when resource identity must be positional — use count only when order/index is semantically meaningful (rare).
- Terragrunt when the project has a single environment — the overhead exceeds the benefit below ~3 environments.

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
