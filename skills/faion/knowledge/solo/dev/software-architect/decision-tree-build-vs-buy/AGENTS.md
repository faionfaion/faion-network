---
slug: decision-tree-build-vs-buy
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use this decision tree to decide whether to build custom software or buy/adopt a commercial solution.
content_id: "a5ba3c10d2eaee00"
tags: [decision-tree, build-vs-buy, tco, vendor-evaluation, make-or-buy]
---
# Build vs Buy Decision Tree

## Summary

**One-sentence:** Use this decision tree to decide whether to build custom software or buy/adopt a commercial solution.

**One-paragraph:** Use this decision tree to decide whether to build custom software or buy/adopt a commercial solution. Routes by strategic importance first, then TCO, time-to-value, and integration complexity. The 3-year TCO comparison is mandatory for any non-trivial decision.

## Applies If (ALL must hold)

- Evaluating a new capability where both custom development and commercial solutions exist.
- Reviewing an existing custom-built solution to assess whether a commercial alternative now makes more sense.
- Justifying a build decision to stakeholders — the tree output serves as the structured rationale.
- Filtering vendor options: the tree shortlists to 2-3 candidates for a full vendor evaluation matrix.

## Skip If (ANY kills it)

- No commercial solutions exist — build is the only option; skip to implementation planning.
- The capability is already built and working well — evaluate only at planned technology review intervals.
- Trivial tooling (CLI helper, one-off script) — the overhead of running the tree exceeds the value.

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

- parent skill: `solo/dev/software-architect/`
