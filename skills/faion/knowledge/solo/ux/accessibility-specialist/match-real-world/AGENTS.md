---
slug: match-real-world
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Users encounter unfamiliar jargon and technical terms.
content_id: "f297804d45736088"
tags: [usability-heuristic, language, ux, conventions, localization]
---
# Match Between System and Real World

## Summary

**One-sentence:** Users encounter unfamiliar jargon and technical terms.

**One-paragraph:** Users encounter unfamiliar jargon and technical terms. Icons and labels do not match what users expect. Information is organized in system-centric rather than user-centric ways. Concepts from the real world are misrepresented or ignored. Without matching the real world: user confusion, learning curve increases, errors from misunderstanding, reduced adoption.

## Applies If (ALL must hold)

- Content audit: reviewing all UI labels, error messages, and instructions for technical language
- Localization prep: ensuring terminology matches user vocabulary before translation
- Error message redesign: replacing system-generated error codes with plain language
- Onboarding copy review: new users encounter the most jargon because they lack domain context
- B2B product launches into a new industry vertical: the same feature may need entirely different terminology for finance vs. healthcare vs. logistics users

## Skip If (ANY kills it)

- Developer tools and CLIs intentionally targeted at technical users — technical language is correct for the audience
- Internal admin panels where all users are trained staff familiar with system terminology
- When users have explicitly indicated they prefer technical precision over simplicity (e.g., API documentation)

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
