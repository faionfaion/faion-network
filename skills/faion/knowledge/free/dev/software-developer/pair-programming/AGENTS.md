---
slug: pair-programming
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A practice where two programmers share one workstation: the Driver writes code while the Navigator reviews each line, thinks strategically, and catches errors.
content_id: "320bd3547e385721"
tags: [pairing, collaboration, knowledge-transfer, tdd, ai-navigator]
---
# Pair Programming

## Summary

**One-sentence:** A practice where two programmers share one workstation: the Driver writes code while the Navigator reviews each line, thinks strategically, and catches errors.

**One-paragraph:** A practice where two programmers share one workstation: the Driver writes code while the Navigator reviews each line, thinks strategically, and catches errors. Pairs switch roles frequently. Four modes: classic Driver-Navigator, Ping-Pong (TDD), Strong-Style (idea must go through the other person's hands), and Tour Guide (expert narrates codebase to newcomer). With an AI agent, the human is always physically the driver; the agent acts as strategic navigator emitting one bounded instruction per turn.

## Applies If (ALL must hold)

- Complex or unfamiliar code areas where a second perspective prevents wrong-path investment.
- Knowledge transfer: onboarding, cross-training, tour guide through legacy code.
- Critical business logic where correctness matters more than speed.
- TDD ping-pong to stay engaged and alternate test/impl roles.
- AI-assisted pairing: human drives, Claude navigates in strong-style mode.

## Skip If (ANY kills it)

- Simple, routine tasks where overhead exceeds benefit.
- Privacy-sensitive code that cannot leave the local machine — skip cloud agent.
- High-velocity sprints where per-line explanation slows the team below solo velocity.
- Domains where the model is weak (DSP, embedded firmware, niche DSLs) — agent adds noise.
- True multi-developer pairing — adding an agent to a human-human pair fragments attention.

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

- parent skill: `free/dev/software-developer/`
