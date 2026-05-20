---
slug: living-documentation
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Living Documentation (Docs-as-Code) treats documentation as a versioned artifact co-located with source code, auto-generated from code where possible, validated in CI, and never manually edited in the auto-generated sections.
content_id: "afaa0a06519cf46d"
tags: [docs-as-code, documentation, ci-cd, devops, quality-gates]
---
# Living Documentation

## Summary

**One-sentence:** Living Documentation (Docs-as-Code) treats documentation as a versioned artifact co-located with source code, auto-generated from code where possible, validated in CI, and never manually edited in the auto-generated sections.

**One-paragraph:** Living Documentation (Docs-as-Code) treats documentation as a versioned artifact co-located with source code, auto-generated from code where possible, validated in CI, and never manually edited in the auto-generated sections. ADRs and design rationale remain hand-authored. API reference, changelogs, and link validity are automated. Every auto-generated section is tagged `` so agents and humans know not to overwrite it manually.

## Applies If (ALL must hold)

- Setting up a new project's documentation pipeline: generator, CI pipeline, auto-generated API reference
- When documentation has drifted from code: regenerate API reference from OpenAPI spec
- When onboarding a new agent: living docs (especially llms.txt and structured README) reduce hallucination
- When deploying a developer portal that surfaces service ownership and runbooks

## Skip If (ANY kills it)

- Internal ADRs and design rationale — must remain manually authored; auto-generated "why" is always wrong
- User-facing marketing copy — optimized for accuracy, not persuasion
- Projects to be archived within 3 months — infrastructure investment exceeds value
- Teams without code review discipline — Docs-as-Code requires the same PR review rigor as code PRs

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

- parent skill: `solo/sdd/sdd/`
