---
slug: mob-programming
tier: free
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Whole-team real-time collaboration: 3–8 people sharing one screen, rotating driver every 5–15 minutes, all others navigating.
content_id: "aaaac3d98c397e53"
tags: [mob-programming, pair-programming, collaboration, agent-integration, team-practice]
---
# Mob Programming

## Summary

**One-sentence:** Whole-team real-time collaboration: 3–8 people sharing one screen, rotating driver every 5–15 minutes, all others navigating.

**One-paragraph:** Whole-team real-time collaboration: 3–8 people sharing one screen, rotating driver every 5–15 minutes, all others navigating. The strong-style rule (idea must pass through the driver's hands) eliminates knowledge silos, catches bugs before typing, and shares context in real time. With agents: cap mob at 4 humans + 1 agent, assign a human facilitator, and rotate the agent on the same timer as humans.

## Applies If (ALL must hold)

- Complex features requiring multiple perspectives simultaneously.
- Critical system changes with high blast radius.
- Team onboarding and knowledge leveling.
- "Impossible" bugs that have stumped individuals.
- Learning mob: team encounters an unfamiliar API or framework.
- Mixed human-AI mob: agent plays navigator or driver for one rotation.

## Skip If (ANY kills it)

- Simple, well-understood, parallelizable tasks — mob overhead is not justified.
- Quiet/individual deep-work tasks — the format itself is wrong.
- Sensitive material (security audits, PII, unreleased secrets) where streaming to an agent creates compliance risk.
- Teams new to both mobbing and agents — double the failure modes; try human-only mobbing first.

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
