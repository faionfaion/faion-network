---
slug: spec-requirements
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured methodology for translating a plain-language feature request into a traceable set of user personas, INVEST-validated user stories, SMART functional and non-functional requirements (FR-X / NFR-X), and Given-When-Then acceptance criteria (AC-X).
content_id: "42340492541ac680"
tags: [sdd, requirements, specifications, smart, moscow]
---
# Specification Requirements

## Summary

**One-sentence:** A structured methodology for translating a plain-language feature request into a traceable set of user personas, INVEST-validated user stories, SMART functional and non-functional requirements (FR-X / NFR-X), and Given-When-Then acceptance criteria (AC-X).

**One-paragraph:** A structured methodology for translating a plain-language feature request into a traceable set of user personas, INVEST-validated user stories, SMART functional and non-functional requirements (FR-X / NFR-X), and Given-When-Then acceptance criteria (AC-X). Every FR must trace to a user story; every Must FR must have at least one AC. Output is a spec.md that the design phase consumes.

## Applies If (ALL must hold)

- Starting any non-trivial feature estimated to touch more than one system layer
- Stakeholder has described a need in plain language that needs translation into testable requirements
- Feature scope is ambiguous and "Out of Scope" must be made explicit before design begins
- Multiple user personas are affected and their needs conflict or overlap
- Acceptance criteria will drive automated BDD tests (Gherkin/Given-When-Then)

## Skip If (ANY kills it)

- Bug fix with a clear, agreed-upon fix — spec overhead exceeds value
- Purely internal refactor with no user-facing behavior change
- Spike or proof-of-concept — spec assumes known requirements; spikes discover them
- Design is already finalized and requirements are back-filled without intent to use them

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
