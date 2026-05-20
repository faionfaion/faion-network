---
slug: spec-examples-basic
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Condensed spec format for MVP features with clear, well-understood requirements.
content_id: "eddc3ed9640addd4"
tags: [spec, condensed, mvp, example, sdd]
---
# Specification Examples: Basic

## Summary

**One-sentence:** Condensed spec format for MVP features with clear, well-understood requirements.

**One-paragraph:** Condensed spec format for MVP features with clear, well-understood requirements. Reduces the full spec-structure v2.0 to five minimum sections: Problem Statement, User Stories (max 3), Functional Requirements (Must only), Acceptance Criteria (1 happy path + 1 error), Out of Scope. Typical size: 1100–1650 tokens.

## Applies If (ALL must hold)

- MVP features with clear requirements (≤ 5 FRs, ≤ 3 User Stories).
- Simple CRUD operations or well-known patterns (auth, registration, forms).
- Small team, fast iteration environment.
- Proof of concept or rapid prototyping.

## Skip If (ANY kills it)

- Features with multiple user personas and complex business rules — use spec-structure full v2.0 instead.
- Regulated domains (payments, healthcare, legal) where traceability completeness is non-negotiable.
- Features with more than 5 User Stories or 10 Functional Requirements.
- Security-sensitive features where at least an unauthorized-access AC is required (condensed ACs are too thin).

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
