---
slug: prototyping
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prototyping is the practice of building interactive representations of a product — from paper sketches to code — at the fidelity level required to answer a specific learning objective before committing to production development.
content_id: "f5bac879df67c033"
tags: [prototyping, interaction-design, usability-testing, design-validation, figma]
---
# Prototyping

## Summary

**One-sentence:** Prototyping is the practice of building interactive representations of a product — from paper sketches to code — at the fidelity level required to answer a specific learning objective before committing to production development.

**One-paragraph:** Prototyping is the practice of building interactive representations of a product — from paper sketches to code — at the fidelity level required to answer a specific learning objective before committing to production development. Static designs cannot convey how interactions behave, which means usability issues remain hidden until expensive development is underway. Prototypes surface these issues early, align stakeholders on expected behavior, and provide a testable artifact for usability research — at a fraction of the cost of discovering the problem in production.

## Applies If (ALL must hold)

- Validating interaction flows before writing production code
- Presenting design concepts to stakeholders who cannot read wireframes
- Running usability tests when no real product exists yet
- Deciding between two competing UX patterns before committing to development
- Documenting expected behavior for handoff to engineers

## Skip If (ANY kills it)

- When the feature scope is a single static content page with no interaction
- When a fully working staging environment already exists and can be tested directly
- When the only unknown is visual aesthetics — use static mockups instead
- When the timeline is so compressed that prototype iteration would delay the actual build

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

- parent skill: `solo/ux/ui-designer/`
