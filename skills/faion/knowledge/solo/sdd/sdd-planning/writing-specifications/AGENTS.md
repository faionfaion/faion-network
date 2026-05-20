---
slug: writing-specifications
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured 9-phase process for writing spec.
content_id: "4a0eca19120a99d7"
tags: [specification, requirements, sdd, smart-criteria, user-stories]
---
# Writing Specifications

## Summary

**One-sentence:** A structured 9-phase process for writing spec.

**One-paragraph:** A structured 9-phase process for writing spec.md — the document that answers "WHAT are we building and WHY?" before design or implementation begins. Covers problem analysis, user personas, user story mapping, SMART functional and non-functional requirements, Given-When-Then acceptance criteria, and explicit scope boundaries.

## Applies If (ALL must hold)

- Feature is new and requirements have not been written down anywhere.
- Existing feature needs scope expansion and the current spec is absent or too vague to drive design.
- Stakeholder and developer have different mental models of what the feature does.
- Requirements exist informally (Slack messages, verbal agreements) and need to be formalized.
- Constitution is new and needs to capture tech decisions before development begins.

## Skip If (ANY kills it)

- Bug report with a clear reproduction path — write a task directly, not a spec.
- Infrastructure change (server config, deployment pipeline) with no user-visible behavior.
- Feature already has an approved spec — open and amend it rather than rewriting from scratch.
- Experiment/spike where the output will determine whether to proceed at all.

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
