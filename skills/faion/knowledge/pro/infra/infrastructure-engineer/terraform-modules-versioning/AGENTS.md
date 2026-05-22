---
slug: terraform-modules-versioning
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Published Terraform modules MUST use Semantic Versioning (SemVer) with Git tags, version constraints on every module source reference, and a maintained CHANGELOG.
content_id: "47cdd9061d6d6936"
tags: [terraform, modules, versioning, semver, registry]
---
# Terraform Module Versioning

## Summary

**One-sentence:** Published Terraform modules MUST use Semantic Versioning (SemVer) with Git tags, version constraints on every module source reference, and a maintained CHANGELOG.

**One-paragraph:** Published Terraform modules MUST use Semantic Versioning (SemVer) with Git tags, version constraints on every module source reference, and a maintained CHANGELOG.md. Without pinned version constraints, a module update can silently break all consumers on the next terraform init.

## Applies If (ALL must hold)

- Authoring a module consumed by more than one caller (team-shared or registry module).
- Upgrading a module dependency — need to understand what constraint syntax is safe.
- Releasing a new module version — need the correct tag and CHANGELOG format.
- Setting up a new consumer module call — choosing the right version constraint operator.

## Skip If (ANY kills it)

- Private local modules referenced by relative path (./modules/vpc) in a mono-repo — they have no separate release lifecycle.
- Single-team repos where the module author and all callers commit in the same branch — version pinning adds overhead without benefit.

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
