---
slug: generative-ui-design
tier: geek
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use AI tools (Galileo, Uizard, v0, Claude Artifacts, Relume) to generate multiple UI layout variants from a feature brief, then have a human select and refine.
content_id: "2bed50277e88ba86"
tags: [generative, ui, design, ai, prototyping]
---
# Generative UI Design

## Summary

**One-sentence:** Use AI tools (Galileo, Uizard, v0, Claude Artifacts, Relume) to generate multiple UI layout variants from a feature brief, then have a human select and refine.

**One-paragraph:** Use AI tools (Galileo, Uizard, v0, Claude Artifacts, Relume) to generate multiple UI layout variants from a feature brief, then have a human select and refine. Generative UI accelerates ideation and rapid prototyping; it does not produce production-ready output. Claude Artifacts is the only agent-native path — the agent generates the artifact inline, the human reviews it, and the agent iterates based on feedback.

## Applies If (ALL must hold)

- Rapid ideation: generating 5–10 UI layout variants from a feature brief before any human design work starts
- Converting a written product spec into interactive prototypes for early stakeholder feedback
- Producing low-fidelity wireframe candidates that a designer then refines
- Generating alternative component implementations (card, list, grid) when the team is undecided
- Bootstrapping a new screen when design system tokens are already defined

## Skip If (ANY kills it)

- Final, production-ready UI is expected — generative output requires significant designer refinement
- Strict brand compliance is mandatory from the first iteration — AI tools ignore brand guidelines unless explicitly constrained
- Component must integrate with an existing codebase — generated code often uses different component libraries
- WCAG AA/AAA accessibility is non-negotiable from day one — generated UIs consistently miss aria attributes and focus management
- The client or legal team cannot review IP of AI-generated design artifacts

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

- parent skill: `geek/ux/ui-designer/`
