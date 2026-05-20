---
slug: help-documentation
tier: solo
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Users who cannot find answers give up, generating support costs and reducing adoption.
content_id: "b671f2e6b5bbc8a0"
tags: [help-systems, documentation, ux, support, content]
---
# Help and Documentation

## Summary

**One-sentence:** Users who cannot find answers give up, generating support costs and reducing adoption.

**One-paragraph:** Users who cannot find answers give up, generating support costs and reducing adoption. Help content reduces friction only when it is discoverable at the moment of confusion, written in user language (not product-team language), and maintained in sync with the actual UI.

## Applies If (ALL must hold)

- Writing or auditing in-app help content: tooltips, empty states, onboarding tours, inline hints
- Generating knowledge base articles or how-to guides from product specs or changelogs
- Auditing existing documentation for staleness, gaps, or coverage against support ticket patterns
- Building a help search index from existing markdown/docs content
- Creating contextual help copy for complex forms, settings pages, or error states

## Skip If (ANY kills it)

- Replacing interface design improvements — if the UI requires a tooltip to be understood, the UI is broken first
- Producing final user-facing copy without human editorial review (accuracy and tone)
- Generating API reference documentation without code-level context (hallucination risk on technical details)
- Substituting for user research on what users actually struggle with — support ticket analysis must precede content strategy

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

- parent skill: `solo/ux/accessibility-specialist/`
