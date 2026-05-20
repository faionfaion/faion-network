---
slug: writing-design-documents
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A design document answers HOW to build a feature by recording architectural decisions (AD-X), file structure, data models, and API contracts before implementation begins.
content_id: "2c73123f27f6b9f6"
tags: [design, architecture, sdd, decisions]
---
# Writing Design Documents

## Summary

**One-sentence:** A design document answers HOW to build a feature by recording architectural decisions (AD-X), file structure, data models, and API contracts before implementation begins.

**One-paragraph:** A design document answers HOW to build a feature by recording architectural decisions (AD-X), file structure, data models, and API contracts before implementation begins. Required when a feature touches 5+ files, changes a DB schema, modifies an API contract, or introduces cross-service dependencies. Every FR-X must trace to at least one AD-X, and every AD-X must list alternatives considered.

## Applies If (ALL must hold)

- After spec.md is approved and before writing implementation-plan.md.
- Feature touches 5+ files, changes a DB schema, modifies an API contract, or has cross-service dependencies.
- When the team needs an explicit record of alternatives considered to prevent re-litigating decisions.
- When onboarding a new agent into an existing codebase — design.md gives full architectural context.

## Skip If (ANY kills it)

- Bug fixes touching 1-2 files with no architectural impact.
- Small refactors with no interface changes.
- Features whose entire scope fits in a single task under ~5k tokens.
- Greenfield experiments or spikes where the design is deliberately exploratory.

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

- parent skill: `solo/sdd/sdd/`
