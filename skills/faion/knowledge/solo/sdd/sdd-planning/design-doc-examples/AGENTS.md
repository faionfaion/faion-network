---
slug: design-doc-examples
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Concrete, worked design document examples for user authentication and related features.
content_id: "e171665d0cc27a17"
tags: [design, architecture-decision, examples, authentication, sdd]
---
# Design Document Examples

## Summary

**One-sentence:** Concrete, worked design document examples for user authentication and related features.

**One-paragraph:** Concrete, worked design document examples for user authentication and related features. Provides a reference AD (Architecture Decision) format with FR traceability tables, file change tables, and component breakdowns that agents use as few-shot structural references when generating or reviewing design.md files.

## Applies If (ALL must hold)

- Generating a new design.md for a user-identity or auth-related feature — inject the auth example as few-shot context.
- Reviewing a generated design.md for structural gaps — compare AD format, FR coverage, and file table against the example.
- Onboarding a new design-writing agent that needs a calibration reference before its first real feature.
- Teaching the AD alternatives-and-rejection pattern when an agent produces shallow "alternatives" sections.

## Skip If (ANY kills it)

- Copying example task names, file paths, or technology choices (JWT, bcrypt cost 12) into a real project without checking the constitution — examples encode defaults, not decisions.
- Frontend component hierarchy examples (RegisterForm props) in backend-only or non-React projects.
- Treating example file structures as required layouts rather than illustrative patterns.
- Running examples through automated tooling that expects live code — they are documentation artifacts, not executable code.

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
