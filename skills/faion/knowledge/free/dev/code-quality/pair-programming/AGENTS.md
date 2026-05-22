---
slug: pair-programming
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A practice where two developers share a single workstation — one drives, one navigates.
content_id: "320bd3547e385721"
tags: [pairing, collaboration, code-review, knowledge-transfer, tdd]
---
# Pair Programming

## Summary

**One-sentence:** A practice where two developers share a single workstation — one drives, one navigates.

**One-paragraph:** A practice where two developers share a single workstation — one drives, one navigates. Roles switch every 15–30 minutes. Three main styles: driver-navigator, ping-pong (TDD), strong-style. With agents the same styles apply; declare style explicitly at session start.

## Applies If (ALL must hold)

- Complex or unfamiliar code where a second perspective catches assumptions.
- Knowledge transfer: onboarding a new team member or cross-training on an unfamiliar module.
- Critical business logic that benefits from real-time review.
- Debugging a hard-to-reproduce issue.
- Agent acting as navigator: rubber-duck escalation with questions and edge-case prompts.
- TDD ping-pong: agent writes one failing test, human makes it pass, human writes next test.

## Skip If (ANY kills it)

- Simple, well-specified, mechanical tasks — agent is overhead; delegate directly.
- Tasks where deliberate struggle is the goal (interview prep, learning by doing) — agent removes useful friction.
- Regulatory code requiring two human sign-offs; agent can advise but cannot fill the human-approver role.
- Long architectural debates — agent sycophantically agrees; use brainstorm instead.
- Sessions longer than 90–120 minutes without breaks; context degrades for both agent and human.

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

- parent skill: `free/dev/code-quality/`
