---
slug: architecture-decision-records
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A single-file document (Nygard format) that captures one architectural decision — its context, the decision made, alternatives considered with rejection reasons, and consequences (positive, negative, neutral).
content_id: "e04a1ee4ff81d8de"
tags: [architecture, adr, decision-records, documentation, agentic-workflow]
---
# Architecture Decision Records (ADR)

## Summary

**One-sentence:** A single-file document (Nygard format) that captures one architectural decision — its context, the decision made, alternatives considered with rejection reasons, and consequences (positive, negative, neutral).

**One-paragraph:** A single-file document (Nygard format) that captures one architectural decision — its context, the decision made, alternatives considered with rejection reasons, and consequences (positive, negative, neutral). ADRs live in docs/adr/NNN-title.md, are numbered sequentially from 001, and transition through statuses: Proposed → Accepted → Deprecated/Superseded. New ADRs amend, never edit, existing Accepted ones.

## Applies If (ALL must hold)

- Before committing to a tech stack choice that will be hard to reverse (database, framework, auth strategy).
- After a production incident that exposes a design weakness — capture the fix decision.
- When a new team member keeps asking "why did we choose X?" — ADR is the answer.
- Anytime two or more viable alternatives were seriously considered.
- At the start of a new feature with meaningful architectural surface (new service, new API contract, new data model).

## Skip If (ANY kills it)

- Trivial implementation details (which library function to call, naming conventions).
- Decisions that will certainly be revisited within 1-2 weeks — too early, no context yet.
- Configuration values that belong in docs, not decision records.
- When there was only one realistic option — no choice means no ADR needed.

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
