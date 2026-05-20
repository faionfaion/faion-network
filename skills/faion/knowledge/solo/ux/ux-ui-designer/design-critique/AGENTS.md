---
slug: design-critique
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific and actionable feedback.
content_id: "8b7a846ace9e56ef"
tags: [design-critique, feedback, design-review, collaboration, async]
---
# Design Critique

## Summary

**One-sentence:** Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific and actionable feedback.

**One-paragraph:** Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific and actionable feedback. Every piece of feedback must follow: Observation → Principle/Goal → Impact → (Optional suggestion). Feedback not tied to a stated goal is opinion, not critique.

## Applies If (ALL must hold)

- Pre-session preparation: generating a structured critique brief from design goals and constraints
- Async critique: reviewing a design description against stated goals and producing structured feedback
- Post-session synthesis: organizing critique notes into prioritized action items
- Solo work: using an agent as a structured sounding board when no human reviewers are available
- Training designers to give and receive goal-based feedback

## Skip If (ANY kills it)

- Replacing human critique sessions — critique is partly a social alignment process that builds shared design language
- When design goals are undefined — critique without objectives degrades to preference-based feedback
- Final production polish decisions — agent cannot assess micro-interaction feel or animation timing
- When stakeholder buy-in is the primary goal — human-led critique creates co-ownership

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
