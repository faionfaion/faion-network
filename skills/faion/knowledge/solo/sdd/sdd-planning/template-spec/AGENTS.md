---
slug: template-spec
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A fill-in-the-blanks template for spec.
content_id: "90e6e806771848c7"
tags: [spec, template, requirements, acceptance-criteria, moscow]
---
# Template: Specification

## Summary

**One-sentence:** A fill-in-the-blanks template for spec.

**One-paragraph:** A fill-in-the-blanks template for spec.md — the document that answers "WHAT are we building and WHY?" Sections: Reference Documents, Overview, Problem Statement (Who/Problem/Impact/Solution/Metric), User Personas, User Stories (As a/I want/So that), Functional Requirements table (FR-X with MoSCoW), Non-Functional Requirements table (NFR-X with targets), Acceptance Criteria (Given-When-Then), Out of Scope table, Assumptions and Constraints, and Dependencies.

## Applies If (ALL must hold)

- Starting any new feature that will be executed by a subagent — the template enforces the FR/AC structure the executor needs
- When a stakeholder provides fuzzy requirements and you need a structured artifact to validate understanding
- Before writing design.md — spec must exist and be approved first
- Generating spec drafts from user interviews, chat logs, or product briefs

## Skip If (ANY kills it)

- Hot-fixes and patches — spec overhead exceeds value for changes under ~2 hours of work
- Pure infrastructure tasks with no user-facing behavior
- Research spikes where requirements are deliberately undefined

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
