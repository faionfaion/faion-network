---
slug: design-doc-advanced-patterns
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Extends a base design document with six advanced sections: component hierarchy (frontend), dependency table (new packages and external services), security mitigations table, performance considerations table, test pyramid strategy, and migration/rollback plan.
content_id: "87ed0297953bfd51"
tags: [design-doc, architecture, advanced-patterns, security, performance]
---
# Design Document Advanced Patterns

## Summary

**One-sentence:** Extends a base design document with six advanced sections: component hierarchy (frontend), dependency table (new packages and external services), security mitigations table, performance considerations table, test pyramid strategy, and migration/rollback plan.

**One-paragraph:** Extends a base design document with six advanced sections: component hierarchy (frontend), dependency table (new packages and external services), security mitigations table, performance considerations table, test pyramid strategy, and migration/rollback plan. Each section traces back to FR-X or NFR-X items from the spec. Performance targets must come from spec NFRs. Security mitigations must reference AD-X decisions.

## Applies If (ALL must hold)

- Feature has a frontend component with more than 2 nesting levels in the component hierarchy.
- Security attack surface requires explicit mitigation table (auth, XSS, CSRF, injection).
- New external dependencies or third-party services are introduced.
- Performance targets are specified in NFRs and must be traced to design decisions.
- Feature involves database schema changes or backward compatibility concerns.
- Full test pyramid (unit + integration + E2E) must be planned at design time.

## Skip If (ANY kills it)

- Pure backend feature with no UI. Skip the component hierarchy section entirely.
- Greenfield project with no existing patterns. Establish base design patterns first; advanced patterns assume known constraints.
- Spike output. Advanced patterns assume known NFRs; spikes produce NFRs, not consume them.
- Security section would be identical to a recently completed feature. Reference the prior design.md instead of duplicating.

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

- parent skill: `solo/sdd/sdd-planning/`
