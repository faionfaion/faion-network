---
slug: use-case-mapping
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Products get built without clear understanding of how users will actually use them.
content_id: "6bb75b23c66cb654"
tags: [research, use-cases, requirements, user-flows, specifications]
---
# Use Case Mapping

## Summary

**One-sentence:** Products get built without clear understanding of how users will actually use them.

**One-paragraph:** Products get built without clear understanding of how users will actually use them. Features become disconnected from real workflows, critical paths are missed, edge cases overlooked until production, and teams lack shared understanding. Use case mapping documents specific ways users interact with your product to achieve goals. It answers: What exactly will users do with this? By defining actors, goals, preconditions, main flows, alternatives, and postconditions, you create a shared understanding across business, engineering, and QA.

## Applies If (ALL must hold)

- Translating validated user research into specifications engineering can build from.
- Drafting acceptance criteria when stories are too thin and edge cases are missed in production.
- Cross-team alignment: business, engineering, and QA need a shared model of what users do and what the system must support.
- Compliance or regulated domains where alternative flows must be explicit and documented.

## Skip If (ANY kills it)

- Pre-discovery: writing use cases before validating problem produces fiction and wastes effort.
- For purely internal scripts or dev tooling where the overhead of documentation exceeds the benefit.
- For exploratory prototyping where requirements are intentionally fuzzy and changing daily.
- When the team uses Jobs-to-Be-Done plus user-story-mapping already; pick one model, not three competing frameworks.

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

- parent skill: `solo/research/researcher/`
