---
slug: release-planning
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six-step process for deciding what goes into each release, when it ships, and how it is communicated.
content_id: "68460e3733a2e87f"
tags: [release-planning, release-management, versioning, rollback, release-notes, semver, changelog]
---
# Release Planning

## Summary

**One-sentence:** Six-step process for deciding what goes into each release, when it ships, and how it is communicated.

**One-paragraph:** Six-step process for deciding what goes into each release, when it ships, and how it is communicated. Covers release-type taxonomy (major/minor/patch/hotfix per SemVer 2.0), readiness checklists, rollback requirements, and audience-specific communication plans. Concrete rule: every release needs a goal statement, a one-command rollback plan, and a communication plan before code touches production.

## Applies If (ALL must hold)

- Planning what to include in an upcoming version (major, minor, patch, or hotfix).
- Coordinating release timing across engineering, support, and marketing for a SaaS or library.
- Writing release notes for an existing set of merged changes that have not yet shipped.
- Setting up a repeatable release cadence for a solo founder or small team.
- Triggers: tag matches `v*`, CHANGELOG `[Unreleased]` is non-empty, milestone closes, customer-visible breaking change is queued.

## Skip If (ANY kills it)

- Continuous deployment with feature flags — individual flag rollouts replace release bundling.
- Pre-launch products with no users — use a task list, not a release plan.
- Emergency hotfixes under time pressure — jump straight to the hotfix subset (steps 3, 5, 6 only).
- Internal-only refactors with no observable surface area — push through the regular CI/CD pipeline.

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

- parent skill: `solo/product/product-planning/`
