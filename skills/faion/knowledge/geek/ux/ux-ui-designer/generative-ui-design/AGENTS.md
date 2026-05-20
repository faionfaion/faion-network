---
slug: generative-ui-design
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for using AI generation tools (v0 by Vercel, Claude Artifacts, Galileo, Uizard, Relume) to produce multiple UI variants rapidly in the ideation phase.
content_id: "2bed50277e88ba86"
tags: [generative-ai, ui-design, ideation, variant-generation, accessibility]
---
# Generative UI Design

## Summary

**One-sentence:** Methodology for using AI generation tools (v0 by Vercel, Claude Artifacts, Galileo, Uizard, Relume) to produce multiple UI variants rapidly in the ideation phase.

**One-paragraph:** Methodology for using AI generation tools (v0 by Vercel, Claude Artifacts, Galileo, Uizard, Relume) to produce multiple UI variants rapidly in the ideation phase. The loop is: agent generates 3–5 variants → human selects and critiques → agent refines → human verifies accessibility → done. Generated output is a forcing function for critique, not a finished deliverable.

## Applies If (ALL must hold)

- Rapid ideation: generating 5–10 UI variants from a brief to explore design space
- Prototyping flows for investor demos or usability tests where visual polish is secondary
- Generating React/HTML component code from design descriptions (v0, Claude Artifacts)
- Reducing blank-canvas paralysis on new projects
- Creating low-fidelity wireframe sets across multiple screen sizes in parallel

## Skip If (ANY kills it)

- Brand-critical production interfaces — AI generation does not understand brand nuance reliably
- Accessibility-first projects — generative outputs routinely miss focus management, ARIA roles, contrast
- Design system contributions — generated components bypass token and variant governance
- When the design problem requires deep user research insight — generation amplifies assumptions
- Final developer handoff — generated code requires significant cleanup before production

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

- parent skill: `geek/ux/ux-ui-designer/`
