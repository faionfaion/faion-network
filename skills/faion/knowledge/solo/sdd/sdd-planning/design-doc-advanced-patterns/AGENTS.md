# Design Document Advanced Patterns

## Summary

Extends a base design document with six advanced sections: component hierarchy (frontend), dependency table (new packages and external services), security mitigations table, performance considerations table, test pyramid strategy, and migration/rollback plan. Each section traces back to FR-X or NFR-X items from the spec. Performance targets must come from spec NFRs — never invented. Security mitigations must reference AD-X decisions.

## Why

Base design docs describe the happy-path architecture. Advanced sections handle the failure modes: XSS, CSRF, SQL injection, rate limiting, database migrations, rollback procedures. Without these sections, implementation teams make ad-hoc security and migration decisions that are inconsistent across features and impossible to review as a unit.

## When To Use

- Feature has a frontend component with more than 2 nesting levels in the component hierarchy
- Security attack surface requires explicit mitigation table (auth, XSS, CSRF, injection)
- New external dependencies or third-party services are introduced
- Performance targets are specified in NFRs and must be traced to design decisions
- Feature involves database schema changes or backward compatibility concerns
- Full test pyramid (unit + integration + E2E) must be planned at design time

## When NOT To Use

- Pure backend feature with no UI — skip the component hierarchy section entirely
- Greenfield project with no existing patterns — establish base design patterns first; advanced patterns assume known constraints
- Spike output — advanced patterns assume known NFRs; spikes produce NFRs, not consume them
- Security section would be identical to a recently completed feature — reference the prior design.md instead of duplicating

## Content

| File | What's inside |
|------|---------------|
| `content/01-advanced-sections.xml` | Rules for component hierarchy, dependency table, security mitigations, performance considerations, test pyramid, migration strategy |
| `content/02-checklist.xml` | Phase-by-phase checklist for producing each advanced section; quality gates per section |

## Templates

none
