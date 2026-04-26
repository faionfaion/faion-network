# Spec Advanced Guidelines

## Summary

Advanced guidelines for writing comprehensive specs for complex, mission-critical features. Full specs have 14 sections: Overview, Problem Statement, Personas, User Stories, Functional Requirements, NFRs, Acceptance Criteria, Out of Scope, Assumptions, Dependencies, Related Features, Skills, Open Questions, Appendix. NFRs must be measurable (< 200ms p95, 99.9% uptime). Acceptance criteria must cover happy path + errors + edge cases + performance + security. Every FR must trace to a user story, every AC to an FR.

## Why

Generic specs produce ambiguous tasks that agents interpret inconsistently. Personas prevent "As a user" antipatterns. Measurable NFRs prevent "system should be fast" antipatterns. Out of Scope prevents scope creep from recurring in every planning session. Traceability chains (FR → US → AC) are the primary quality gate for spec completeness.

## When To Use

- Complex features with multiple user types or roles
- Features with significant NFRs (performance, security, scalability targets)
- Features with external system dependencies or API contracts
- Mission-critical features affecting core business metrics
- Features requiring cross-role alignment (dev + product + design)

## When NOT To Use

- Simple CRUD with no business logic (use minimal spec: Overview + 1-2 stories + basic AC)
- Trivial UI copy changes (inline comment sufficient)
- Internal refactoring without external behavior change (use design doc only)
- Experimental features under development (use lightweight hypothesis spec)

## Content

| File | What's inside |
|------|---------------|
| `content/01-section-rules.xml` | Required sections, persona rules, user story format, FR traceability |
| `content/02-nfr-and-ac.xml` | NFR measurability rules, AC coverage matrix, out-of-scope documentation |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-full-template.md` | 14-section full spec stub |
| `templates/check-traceability.sh` | Shell script to verify FR → US → AC coverage |
