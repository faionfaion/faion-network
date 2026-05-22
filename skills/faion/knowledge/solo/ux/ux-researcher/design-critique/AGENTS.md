---
slug: design-critique
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific, actionable feedback to improve the design.
content_id: "8b7a846ace9e56ef"
tags: [design-critique, feedback, design-review, team-collaboration, design-process]
---
# Design Critique

## Summary

**One-sentence:** Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific, actionable feedback to improve the design.

**One-paragraph:** Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific, actionable feedback to improve the design. Without structure, reviews turn into opinion battles where feedback is vague, ideas are killed by personal preferences, and designs don't improve.

## Applies If (ALL must hold)

- Before handoff from design to development, as a final quality gate against defined design principles.
- During each design sprint iteration when you need structured feedback on a single direction.
- When async critique is needed for distributed teams — a written structured format prevents opinion debates in Slack threads.
- When onboarding junior designers who need a framework for giving and receiving feedback.
- When a design decision has been contested by stakeholders and you need an objective evaluation against goals.

## Skip If (ANY kills it)

- When the problem definition is still open; critique assumes a design direction exists — use brainstorming or co-design workshops instead.
- For pixel-level polish feedback on a concept still in wireframe stage; match feedback stage to design fidelity.
- When the critique group lacks context on the user, the problem, or the constraints — missing context makes feedback opinion-based regardless of the framework.
- As a replacement for user testing; critique surfaces expert opinions, not actual user behavior.

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

- parent skill: `solo/ux/ux-researcher/`
