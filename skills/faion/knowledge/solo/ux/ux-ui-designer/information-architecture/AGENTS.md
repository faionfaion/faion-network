---
slug: information-architecture
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organize content by user tasks and goals.
content_id: "10facf6f10a90242"
tags: [information-architecture, navigation, taxonomy, card-sorting, tree-testing]
---
# Information Architecture

## Summary

**One-sentence:** Organize content by user tasks and goals.

**One-paragraph:** Organize content by user tasks and goals. Produces category structure, taxonomy, sitemap. Validate with card sorting and tree testing.

## Applies If (ALL must hold)

- Generating a sitemap or taxonomy from a product spec, feature list, or content inventory
- Auditing an existing IA against card sort or tree test data to identify mismatches
- Drafting an IA strategy document from user research findings and business requirements
- Proposing navigation label alternatives when current labels test poorly with users

## Skip If (ANY kills it)

- Validating a proposed IA — agents draft structure but cannot replace card sorting and tree testing with real users
- Real-time search relevance tuning — IA shapes browse; search ranking is a separate discipline
- Micro-level layout decisions — IA governs content organization, not component placement within a page

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

- parent skill: `solo/ux/ux-ui-designer/`
