---
slug: ba-requirements-mgmt
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: This methodology covers three sub-disciplines of ongoing requirements stewardship: requirements maintenance (version control, attribute management, quality monitoring, archival strategy), change impact analysis (scope, effort, risk, stakeholder impact, decision support), and requirements architecture (viewpoints, decomposition, dependencies, completeness).
content_id: "e31dc3a4b1616f4f"
tags: [requirements, ba, maintenance, change-impact, architecture]
---
# BA Requirements Management Methodologies

## Summary

**One-sentence:** This methodology covers three sub-disciplines of ongoing requirements stewardship: requirements maintenance (version control, attribute management, quality monitoring, archival strategy), change impact analysis (scope, effort, risk, stakeholder impact, decision support), and requirements architecture (viewpoints, decomposition, dependencies, completeness).

**One-paragraph:** This methodology covers three sub-disciplines of ongoing requirements stewardship: requirements maintenance (version control, attribute management, quality monitoring, archival strategy), change impact analysis (scope, effort, risk, stakeholder impact, decision support), and requirements architecture (viewpoints, decomposition, dependencies, completeness). These practices apply after an initial requirement set exceeds ~50 items and human memory cannot track coherence across changes.

## Applies If (ALL must hold)

- Stable product past MVP where the requirement count exceeds ~50 and human memory of "what we agreed" no longer scales — periodic review cadence pays off.
- Change-heavy environments (enterprise integrations, regulated domains) where every CR must be costed and risk-assessed before approval.
- Multi-team systems where one team's requirements depend on another's; you need an explicit dependency graph and viewpoint partitioning to prevent silent conflicts.
- Audit / certification preparation (ISO 9001, SOC2, MDR) where reviewers ask "show me your requirements baseline and how it has changed since last audit".
- Migrating a legacy backlog into a structured architecture (BR → SR → FR decomposition) so AI agents can reason about scope changes.

## Skip If (ANY kills it)

- Pre-PMF / discovery: requirements churn faster than maintenance ceremony can follow; use `continuous-discovery` and disposable RFCs instead.
- Tiny teams (less than 5 people, single product) where Slack + a Linear backlog covers change discussion — formal CIA forms add bureaucracy without payoff.
- Pure agile shops with no contractual requirement baseline; the user-story backlog already encodes scope, and CIA = a 5-minute estimation chat.
- One-shot internal tools or research prototypes — the change cost analysis exceeds the change cost.

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
