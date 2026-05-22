---
slug: prototyping
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Interactive product representation before code.
content_id: "f5bac879df67c033"
tags: [prototyping, ux-design, user-testing, validation, fidelity]
---
# Prototyping

## Summary

**One-sentence:** Interactive product representation before code.

**One-paragraph:** Interactive product representation before code. Pick fidelity by learning goal: concept → paper, flow → clickable, experience → high-fi. Plan, build, test, iterate.

## Applies If (ALL must hold)

- A risky design assumption needs validation before development starts (navigation, onboarding, checkout, auth).
- Stakeholders disagree on how a flow should work, not just how it looks.
- The design brief contains 3+ open questions about user behaviour the team cannot answer from data.
- The team must choose between two or more interaction patterns and needs evidence.
- Generating a structured prototype plan and usability test script from a design brief.
- Code prototype is needed to validate technical feasibility (animation perf, gesture handling).

## Skip If (ANY kills it)

- The interaction is motion-dependent or too nuanced for text-based planning (agent can plan, not build).
- A live coded prototype is required and crosses from UX planning into implementation.
- No clear testing hypothesis exists — prototyping without defined learning goals wastes cycles.
- Post-launch optimization where A/B testing or analytics provide faster signal at lower cost.
- The flow already ships and quantitative product analytics (heatmaps, funnel data) are available.

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

- parent skill: `solo/ux/ux-ui-designer/`
