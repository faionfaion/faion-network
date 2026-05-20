---
slug: requirements-lifecycle
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Requirements exist in multiple versions with unclear ownership, approved requirements change without process, and implementations diverge from documentation.
content_id: "f7993c25c1bff05e"
tags: [requirements, lifecycle, babok, business-analysis, change-control]
---
# Requirements Lifecycle Management

## Summary

**One-sentence:** Requirements exist in multiple versions with unclear ownership, approved requirements change without process, and implementations diverge from documentation.

**One-paragraph:** Requirements exist in multiple versions with unclear ownership, approved requirements change without process, and implementations diverge from documentation. The Requirements Lifecycle Management framework provides six deterministic stages (Identify, Analyze, Specify, Validate, Verify, Manage) with explicit state transitions, version history tracking, change control via impact analysis, and audit trails. Each requirement has a frozen baseline, versioning rules (material scope/AC/NFR changes bump version; wording-only edits do not), and a state machine that tracks Draft → Proposed → Approved → Implemented → Verified with deferred and rejected branches.

## Applies If (ALL must hold)

- The team adopts BABOK Knowledge Area 5 as a working contract and needs formal definitions of stages, states, attributes, and transitions.
- Onboarding junior BAs or agents who must understand state semantics before touching tools.
- Any regulated or audited work where the team must prove that requirements followed a formal process.
- Projects with ≥30 requirements where multiple people are editing; version confusion becomes a bottleneck.
- Establishing the canonical state model that downstream tools (Jira, StrictDoc, Polarion) must conform to.

## Skip If (ANY kills it)

- The team rejects BABOK and runs pure Scrum without formal requirements; use agile-ba-frameworks instead.
- Pre-PMF discovery where the thing under change is the problem statement, not a requirement; use continuous-discovery instead.
- Single-author throwaway work where git log is sufficient version history; lifecycle formality is overhead.
- High-churn research or experimental environments where a 200-change-per-sprint workflow makes formal baselining fiction.
- Small squads (1-2 people) where Proposed → Approved adds ceremony with no value.

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

- parent skill: `pro/ba/ba-core/`
