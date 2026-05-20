---
slug: architecture-decision-records
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ADRs capture significant architectural decisions with context, alternatives, and consequences.
content_id: "e04a1ee4ff81d8de"
tags: [architecture, decision-records, adr, nygard, documentation]
---
# Architecture Decision Records

## Summary

**One-sentence:** ADRs capture significant architectural decisions with context, alternatives, and consequences.

**One-paragraph:** ADRs capture significant architectural decisions with context, alternatives, and consequences. They prevent tribal knowledge loss and stop the same debates from recurring. Store ADRs in version control with code, not in wikis. Keep each ADR to 1-2 pages. Status lifecycle: Proposed → Accepted → Deprecated | Superseded. Never alter an accepted ADR — create a new one to supersede it.

## Applies If (ALL must hold)

- Choosing frameworks, databases, or major dependencies.
- Breaking API changes that require consumer migration.
- Adopting architectural patterns (microservices, event-driven, CQRS).
- Quality attribute tradeoffs (security vs. performance, consistency vs. availability).
- Cross-team decisions affecting multiple services.
- Making implicit standards explicit.

## Skip If (ANY kills it)

- Small, reversible decisions with low risk.
- Implementation details that don't set a pattern.
- Individual bug fixes or minor feature changes.
- Items already covered by existing standards.
- Single-developer, self-contained, minimal-risk choices.

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

- parent skill: `solo/sdd/sdd/`
