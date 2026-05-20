---
slug: template-design
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A fill-in-the-blanks template for design.
content_id: "601f7095198597ac"
tags: [design, template, architecture, adr, fr-coverage]
---
# Template: Design Document

## Summary

**One-sentence:** A fill-in-the-blanks template for design.

**One-paragraph:** A fill-in-the-blanks template for design.md — the document that answers "HOW are we building it?" after spec.md is approved. Covers Reference Documents, Overview, Architecture Decisions (AD-X in ADR format), Components, Data Flow, Data Models, API Endpoints, Files (CREATE/MODIFY), Testing Strategy, Risks, and FR Coverage table.

## Applies If (ALL must hold)

- After spec.md is approved and before writing implementation-plan.md
- Generating a new design.md for any feature driven by approved requirements
- Reviewing an existing design doc for structural completeness against required sections
- Calibrating output format when a new design-writing agent is added to the pipeline

## Skip If (ANY kills it)

- Before spec.md is approved — template fields will be guesswork without grounded requirements
- For a task that affects a single file — full design doc overhead is unjustified; write the task directly
- As a living document — design.md should be frozen after approval; use task files for implementation details
- As a substitute for contracts.md — API endpoints belong in contracts, not in design

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

- parent skill: `solo/sdd/sdd-planning/`
