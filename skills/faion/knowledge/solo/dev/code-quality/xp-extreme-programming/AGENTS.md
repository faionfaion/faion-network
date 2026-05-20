---
slug: xp-extreme-programming
tier: solo
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agile methodology built on 5 values (communication, simplicity, feedback, courage, respect) and 12 practices (TDD, pair programming, collective ownership, CI, small releases, YAGNI).
content_id: "09561b55db549aca"
tags: [extreme-programming, agile, tdd, pair-programming, continuous-integration]
---
# Extreme Programming (XP)

## Summary

**One-sentence:** Agile methodology built on 5 values (communication, simplicity, feedback, courage, respect) and 12 practices (TDD, pair programming, collective ownership, CI, small releases, YAGNI).

**One-paragraph:** Agile methodology built on 5 values (communication, simplicity, feedback, courage, respect) and 12 practices (TDD, pair programming, collective ownership, CI, small releases, YAGNI). The concrete rule: if a practice is good, take it to its logical extreme — if testing is good, test everything first (TDD); if reviews help, review all code via pairing. "Done" means: tests pass, no TODOs, CHANGELOG updated.

## Applies If (ALL must hold)

- Solo developer using Claude as the pair — TDD, simple design, small releases map cleanly to agentic loops.
- Small team (2-12) co-located or strong-sync, building a product with churning requirements.
- Greenfield product where you can enforce coding standards and CI from day one.
- Codebases that already have high test coverage — XP feedback loops only work when the suite is fast and trusted.

## Skip If (ANY kills it)

- Compliance-heavy domains (medical, aerospace) requiring big upfront design and signed change controls.
- Distributed async-only teams that cannot do real-time pairing or daily sync (use Kanban/async Scrum instead).
- Projects without an accessible customer/PM proxy — the on-site customer practice collapses.
- Maintenance-mode systems where pace is dictated by external SLAs, not iterations.

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

- parent skill: `solo/dev/code-quality/`
