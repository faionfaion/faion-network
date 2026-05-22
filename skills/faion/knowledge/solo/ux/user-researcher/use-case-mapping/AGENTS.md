---
slug: use-case-mapping
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use case mapping is documenting specific ways users interact with your product to achieve goals.
content_id: "6bb75b23c66cb654"
tags: [use-cases, research, requirements, user-flows]
---
# Use Case Mapping

## Summary

**One-sentence:** Use case mapping is documenting specific ways users interact with your product to achieve goals.

**One-paragraph:** Use case mapping is documenting specific ways users interact with your product to achieve goals. It answers: "What exactly will users do with this?" This methodology helps teams understand critical user workflows, identify missing features, and ensure comprehensive product design.

## Applies If (ALL must hold)

- Requirements elicitation: translating stakeholder conversations into structured system behavior
- Before writing tickets: ensuring features cover all actors and alternative flows, not just the happy path
- API design: mapping use cases to endpoints before writing any code
- QA test planning: use cases map 1:1 to test scenarios and edge case coverage
- Onboarding new engineers: use case specifications are faster to parse than code for understanding what a system does

## Skip If (ANY kills it)

- During early ideation when scope is still fluid — formalized use cases lock in assumptions too early
- For pure UI/visual design tasks where user flow diagrams (journey maps) communicate better
- For internal batch jobs or background processes with no human actor
- When the team is using BDD with Gherkin — use cases and Gherkin scenarios overlap; pick one to avoid double documentation

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

- parent skill: `solo/ux/user-researcher/`
