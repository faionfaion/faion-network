---
slug: spec-writing
tier: solo
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A product specification (PRD) defines WHAT to build and WHY, leaving HOW to design and engineering.
content_id: "d6ec08c1815839b4"
tags: [product-management, specification, prd, acceptance-criteria, requirements]
---
# Product Specification Writing

## Summary

**One-sentence:** A product specification (PRD) defines WHAT to build and WHY, leaving HOW to design and engineering.

**One-paragraph:** A product specification (PRD) defines WHAT to build and WHY, leaving HOW to design and engineering. Required sections: Overview, Problem, Goals (with current/target metric table), Non-Goals, User Stories (As-a/I-want/So-that with persona IDs), Functional Requirements (FR-N IDs), Non-Functional Requirements, Acceptance Criteria (Given/When/Then per FR), Out of Scope, Open Questions. Every FR must have at least one AC; every goal must be measurable. Spec ends at ~5 pages for most features; beyond that, split or use a Mini-Spec.

## Applies If (ALL must hold)

- Feature is large enough (more than one sprint) that engineers and designers need a shared written contract before work starts.
- Cross-team work where multiple stakeholders must approve scope.
- Building against an external SLA or paid customer commitment requiring traceable requirements.
- Onboarding a contractor—the spec is the briefing artifact.

## Skip If (ANY kills it)

- Tiny changes (less than one day, no ambiguity)—a backlog item with acceptance criteria is sufficient.
- Highly exploratory discovery work where requirements change weekly. Spec the experiment, not the product.
- After implementation as a retroactive document—that is documentation, not a spec.
- When the team will not maintain the spec post-launch; outdated specs mislead more than they help.

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

- parent skill: `solo/product/product-manager/`
