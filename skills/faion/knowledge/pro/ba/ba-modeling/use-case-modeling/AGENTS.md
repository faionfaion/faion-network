---
slug: use-case-modeling
tier: pro
group: ba
domain: ba-modeling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A technique for expressing functional requirements as actor-system interaction sequences.
content_id: "a8b8106842b7d773"
tags: [use-cases, functional-requirements, actor-goals, scenario-modeling, requirements-traceability]
---
# Use Case Modeling

## Summary

**One-sentence:** A technique for expressing functional requirements as actor-system interaction sequences.

**One-paragraph:** A technique for expressing functional requirements as actor-system interaction sequences. Each use case captures WHO achieves WHAT goal with the system and HOW the system responds across normal, alternative, and exception flows. Use case names follow Verb+Noun convention; each has preconditions, a main flow (5-9 steps), alternative flows, exception flows, and postconditions.

## Applies If (ALL must hold)

- Functional requirements for transactional systems (line-of-business apps, regulated software) before development starts
- Multiple actor types interact with the system and cross-actor collisions have already caused bugs
- Compliance/audit context (FDA 21 CFR Part 11, SOX) requiring actor-goal → flow → code → test traceability
- Legacy system migration where screens are reverse-engineered into a controlled spec
- Test engineers need a deterministic scenario source for end-to-end test design
- Pre-development alignment when stakeholders speak features and developers need flows

## Skip If (ANY kills it)

- Pure discovery phase — Opportunity Solution Trees give better signal than premature formalization
- Agile teams operating well with user stories + acceptance criteria — UC specs duplicate work
- Pure data/analytics platforms where data flow models fit better than actor-goal sequences
- ML/LLM features with probabilistic responses — use cases assume deterministic system behavior
- Tiny CRUD apps with one actor and fewer than 10 screens — an acceptance criteria sheet is faster
- Event-driven systems where event topology matters more than actor goals; use event storming or BPMN

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

- parent skill: `pro/ba/ba-modeling/`
