---
slug: match-real-world
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #2: the interface must use words, icons, and organizational patterns that match users' mental models — not internal system or developer terminology.
content_id: "f297804d45736088"
tags: [heuristics, ux-copy, language, mental-models, localization]
---
# Match Between System and Real World

## Summary

**One-sentence:** Nielsen Heuristic #2: the interface must use words, icons, and organizational patterns that match users' mental models — not internal system or developer terminology.

**One-paragraph:** Nielsen Heuristic #2: the interface must use words, icons, and organizational patterns that match users' mental models — not internal system or developer terminology. Replace jargon ("terminate session") with user vocabulary ("log out"). Follow domain conventions (shopping cart, inbox, trash) even when the underlying metaphor is dated. Information must appear in the order users expect, not the order the system processes it.

## Applies If (ALL must hold)

- Auditing UI copy for jargon, abbreviations, or technical terms before a release
- Reviewing API-generated UI strings (error messages, status labels, field names) for plain language
- Localization: verifying translated content matches mental models in the target locale
- When user research reveals confusion about specific labels or navigation terms
- Code review: checking that developer-written placeholder text and labels are user-friendly

## Skip If (ANY kills it)

- Technical admin dashboards used exclusively by engineers — technical language is correct there
- B2B products where users are domain experts who expect precise technical vocabulary
- When user research or A/B tests have already validated the existing language
- Early prototype stages where content is placeholder — audit when real content is set

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
