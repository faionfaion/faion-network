---
slug: recognition-over-recall
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Users must remember information from one part of the interface to use in another.
content_id: "c767d6692d17824a"
tags: [usability-heuristic, cognition, ux, memory-load, accessibility]
---
# Recognition Rather Than Recall

## Summary

**One-sentence:** Users must remember information from one part of the interface to use in another.

**One-paragraph:** Users must remember information from one part of the interface to use in another. They need to recall command syntax or codes. Options are hidden until users know to look for them. Instructions disappear before users can follow them. Memory becomes a barrier to use. Without recognition support: cognitive overload, slower task completion, more errors, frustration.

## Applies If (ALL must hold)

- UI audit: reviewing an existing interface for cognitive load issues
- Design review: checking new component designs before implementation
- Accessibility review: recognition aids are disproportionately important for users with cognitive disabilities
- Command-palette or search interface design: autocomplete and suggestions are the primary recognition mechanism
- Onboarding flow design: new users have zero recall of your UI; every step must surface what to do next

## Skip If (ANY kills it)

- When the interface is exclusively for expert power-users who have internalized shortcuts (e.g., vim, git CLI) — recall is the design intent
- When screen real estate is genuinely constrained (e.g., mobile watch apps) — some hiding is unavoidable; add tooltips
- When adding recognition aids would create visual noise that harms scannability — balance with aesthetic simplicity

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
