---
slug: system-design-process
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A five-phase process (Understand → Scope → Design → Validate → Document) for turning a product brief into a buildable architecture package: requirements list, NFR targets with numeric back-of-envelope estimates, C4 diagrams (L1+L2 minimum), and ADRs per non-obvious decision.
content_id: "3fb0adefc38b829a"
tags: [system-design, architecture-process, nfr, c4-model, adr]
---
# System Design Process

## Summary

**One-sentence:** A five-phase process (Understand → Scope → Design → Validate → Document) for turning a product brief into a buildable architecture package: requirements list, NFR targets with numeric back-of-envelope estimates, C4 diagrams (L1+L2 minimum), and ADRs per non-obvious decision.

**One-paragraph:** A five-phase process (Understand → Scope → Design → Validate → Document) for turning a product brief into a buildable architecture package: requirements list, NFR targets with numeric back-of-envelope estimates, C4 diagrams (L1+L2 minimum), and ADRs per non-obvious decision. LLMs accelerate each phase but require human sign-off at NFR finalization and ADR acceptance.

## Applies If (ALL must hold)

- Greenfield system design where requirements, NFRs, and scale assumptions are still being captured.
- Replacement/replatform decisions that need a spec, ADRs, and C4 diagrams before code.
- Pre-implementation handoff: turning a product brief into a package the dev agent can execute.
- Internal design exercises where a reviewable artifact (not a whiteboard sketch) is the deliverable.

## Skip If (ANY kills it)

- Small bug fixes or localized refactors — overkill; use the relevant pattern methodology directly.
- Prototype/spike code where the goal is to learn, not commit to an architecture.
- Domains the team operates daily (CRUD admin tools) — skip to templates.
- Operational incidents — use reliability-architecture and observability instead.

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

- parent skill: `solo/dev/software-architect/`
