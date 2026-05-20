---
slug: design-docs-patterns
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Write a design document before implementing any feature that takes more than one engineering day.
content_id: "d6aa709989f916a7"
tags: [design-docs, sdd, architecture, writing, patterns]
---
# Design Docs Patterns

## Summary

**One-sentence:** Write a design document before implementing any feature that takes more than one engineering day.

**One-paragraph:** Write a design document before implementing any feature that takes more than one engineering day. Use lightweight Google-style (1-4 pages: context, goals, non-goals, proposed solution, alternatives, open questions) for team-scoped work. Use heavier formats (Amazon 6-pager, Uber RFC) only for cross-org or executive-audience decisions. Always include a non-goals section and at least two genuine alternatives — not strawmen. Set a review deadline when circulating.

## Applies If (ALL must hold)

- Any feature taking more than one engineering day
- Cross-cutting changes affecting multiple modules, services, or teams
- Requirements that are unclear or conflicting — writing exposes gaps
- Generating design.md in the SDD lifecycle (spec → design → test-plan → impl-plan)
- Before proceeding to implementation-plan.md generation — design must be marked Approved

## Skip If (ANY kills it)

- Bug fixes with obvious root cause and one-line solution — PR description is sufficient
- Prototypes and spikes where output is discarded regardless of design quality
- Work taking less than a few hours — overhead exceeds benefit
- Solo purely internal refactors with identical external behavior

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
