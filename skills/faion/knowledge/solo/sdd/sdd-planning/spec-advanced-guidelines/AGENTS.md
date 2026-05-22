---
slug: spec-advanced-guidelines
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced guidelines for writing comprehensive specs for complex, mission-critical features.
content_id: "8d723aec0e9943e8"
tags: [specifications, requirements, acceptance-criteria, nfr, traceability]
---
# Spec Advanced Guidelines

## Summary

**One-sentence:** Advanced guidelines for writing comprehensive specs for complex, mission-critical features.

**One-paragraph:** Advanced guidelines for writing comprehensive specs for complex, mission-critical features. Full specs have 14 sections: Overview, Problem Statement, Personas, User Stories, Functional Requirements, NFRs, Acceptance Criteria, Out of Scope, Assumptions, Dependencies, Related Features, Skills, Open Questions, Appendix. NFRs must be measurable (< 200ms p95, 99.9% uptime). Acceptance criteria must cover happy path + errors + edge cases + performance + security. Every FR must trace to a user story, every AC to an FR.

## Applies If (ALL must hold)

- Complex features with multiple user types or roles
- Features with significant NFRs (performance, security, scalability targets)
- Features with external system dependencies or API contracts
- Mission-critical features affecting core business metrics
- Features requiring cross-role alignment (dev + product + design)

## Skip If (ANY kills it)

- Simple CRUD with no business logic (use minimal spec: Overview + 1-2 stories + basic AC)
- Trivial UI copy changes (inline comment sufficient)
- Internal refactoring without external behavior change (use design doc only)
- Experimental features under development (use lightweight hypothesis spec)

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
