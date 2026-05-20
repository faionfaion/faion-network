---
slug: go-layout-directory-structure
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organize every Go service under a four-directory skeleton: cmd/ (binaries), internal/ (private app code), pkg/ (public libraries), migrations/ (schema files).
content_id: "ea193cb30947c432"
tags: [go, project-structure, directory-layout, backend]
---
# Go Standard Layout — Directory Structure

## Summary

**One-sentence:** Organize every Go service under a four-directory skeleton: cmd/ (binaries), internal/ (private app code), pkg/ (public libraries), migrations/ (schema files).

**One-paragraph:** Organize every Go service under a four-directory skeleton: cmd/ (binaries), internal/ (private app code), pkg/ (public libraries), migrations/ (schema files). The layout is a community convention — not enforced by the toolchain — so teams must agree on it once and commit it to docs.

## Applies If (ALL must hold)

- Greenfield Go services where the team wants a single, agreed-upon directory convention to cut bikeshedding about "where does this go?"
- Mid-size services with multiple binaries (cmd/api, cmd/worker, cmd/migrate) sharing a domain core under internal/.
- Monorepos that need to publish reusable libraries via pkg/ while keeping app code private under internal/.
- Onboarding-heavy teams where a navigable layout matters more than micro-optimisations to package shape.
- Refactoring a "single-package" Go app that grew past ~3k LOC and now wants explicit handler/service/repository seams.

## Skip If (ANY kills it)

- Tiny CLIs (500 LOC or fewer, one binary) — main.go plus a couple of files is sufficient; the layout is a tax.
- Library-only modules — the golang-standards/project-layout doc explicitly states it is not for libraries.
- Teams that have already converged on a different convention (e.g., Domain-driven internal/context/... package-by-feature) — switching mid-flight churns the diff for no win.
- Hyper-optimised single-package code where every package boundary is a string-allocating call.
- Educational or demo repos where the layout obscures the lesson — keep flat.

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

- parent skill: `pro/dev/backend-systems/`
