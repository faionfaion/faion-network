---
slug: tree-testing
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tree testing evaluates the findability of topics in a website's hierarchy by having participants navigate a text-only version of the site structure (no design, no content) to locate answers to scenario tasks.
content_id: "b3b3361955a312cd"
tags: [tree-testing, information-architecture, ia-validation, findability, usability-testing]
---
# Tree Testing

## Summary

**One-sentence:** Tree testing evaluates the findability of topics in a website's hierarchy by having participants navigate a text-only version of the site structure (no design, no content) to locate answers to scenario tasks.

**One-paragraph:** Tree testing evaluates the findability of topics in a website's hierarchy by having participants navigate a text-only version of the site structure (no design, no content) to locate answers to scenario tasks. Key metrics are success rate, directness, and first-click correctness. Requires 30-50 participants for statistical confidence and 10-15 tasks covering shallow and deep destinations.

## Applies If (ALL must hold)

- Validating a proposed IA before visual design or build begins.
- Comparing two candidate IAs head-to-head with the same task set.
- Post-card-sort validation: test that users can navigate the structure card sorting produced.
- Pre-redesign baselining: measure findability on current site vs proposed site to quantify lift.

## Skip If (ANY kills it)

- IA does not yet exist — run a card sort first.
- Testing visual labels, CTAs, or filtering UI — use first-click testing or full usability testing.
- Sites where >50% of traffic enters via search — navigation findability is a weaker signal.
- Single-page apps without hierarchical navigation — there is no tree to test.

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

- parent skill: `pro/ux/ux-researcher/`
