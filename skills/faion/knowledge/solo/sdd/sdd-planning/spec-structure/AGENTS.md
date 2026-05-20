---
slug: spec-structure
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full spec structure v2.
content_id: "17fa97cfdc42e380"
tags: [sdd, specification, structure, quality-gates, requirements]
---
# Specification Structure

## Summary

**One-sentence:** Full spec structure v2.

**One-paragraph:** Full spec structure v2.0 for features with 3+ user personas or 8+ functional requirements. The spec answers WHAT and WHY — never HOW. Mandatory sections: Overview, Problem Statement, User Personas, User Stories, Functional Requirements (FR-X with SMART criteria and MoSCoW priority), Non-Functional Requirements, Acceptance Criteria (Given-When-Then), Out of Scope, Assumptions, Dependencies. Typical size: 500–1200 tokens.

## Applies If (ALL must hold)

- Features with 3+ user personas or 8+ functional requirements
- Features requiring formal stakeholder sign-off where completeness is auditable
- Complex integrations where NFRs (performance, security, scalability) must be contracted before design begins
- When the spec feeds into a multi-agent executor pipeline and full FR/AC traceability is required

## Skip If (ANY kills it)

- MVP features under 5 FRs — use spec-examples-basic condensed format instead
- Internal tooling or developer-only features where user persona sections add no value
- Features on a known pattern (nth CRUD endpoint) where all structural decisions are inherited
- When spec or design doc is still in draft; writing full spec too early wastes tokens when requirements shift

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
