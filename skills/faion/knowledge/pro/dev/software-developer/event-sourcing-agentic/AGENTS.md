---
slug: event-sourcing-agentic
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Drive event-sourcing scaffolding as a five-stage agentic pipeline: aggregate design → code-gen → projection → tests → anti-pattern review.
content_id: "a6bd6549e60887c6"
tags: [event-sourcing, agentic-workflow, ai-agents, code-generation, event-store]
---
# Event Sourcing — Agentic Workflow and Tooling

## Summary

**One-sentence:** Drive event-sourcing scaffolding as a five-stage agentic pipeline: aggregate design → code-gen → projection → tests → anti-pattern review.

**One-paragraph:** Drive event-sourcing scaffolding as a five-stage agentic pipeline: aggregate design → code-gen → projection → tests → anti-pattern review. Key gotchas: agents emit CRUD-style events, mutate state outside apply, and forget expected_version. Prompt patterns and CLI tools listed.

## Applies If (ALL must hold)

- Scaffolding a new event-sourced aggregate from a bounded context spec.
- Reviewing a PR adding event-sourcing code against the anti-pattern checklist.
- Generating projection, repository, and test scaffolding for an existing aggregate design.

## Skip If (ANY kills it)

- Designing event boundaries for an unfamiliar domain — DDD aggregate design requires human domain expertise; the agent assists but cannot own the decisions.
- Deleting or renaming published event classes — always human-reviewed, never auto-merged.

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

- parent skill: `pro/dev/software-developer/`
