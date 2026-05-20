---
slug: strategy-basics
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Framework for understanding the existing environment, defining desired future state, assessing risks, and planning change strategy.
content_id: "e5a27308a5b32788"
tags: [strategy, current-state, future-state, risk-analysis, change-management]
---
# BA Strategy Basics: Current/Future State and Risk

## Summary

**One-sentence:** Framework for understanding the existing environment, defining desired future state, assessing risks, and planning change strategy.

**One-paragraph:** Framework for understanding the existing environment, defining desired future state, assessing risks, and planning change strategy. Covers current state analysis across business context, capability assessment, technology landscape, stakeholder landscape, and SWOT analysis. Future state definition includes vision statements, SMART goals, new capabilities, success metrics, and constraints. Risk analysis covers identification, assessment, response strategy, and monitoring. Change strategy planning includes gap analysis, solution options, transition planning, readiness assessment, and business case development.

## Applies If (ALL must hold)

- Baseline capability and maturity assessment across an organization before planning a transformation initiative
- Business process improvement engagement where the current state is poorly understood and stakeholders disagree on priorities
- Technology modernization decision where cost, risk, and capability trade-offs must be explicit before implementation begins
- Org restructuring or change management engagement where stakeholder landscape and readiness assessment drive the transition strategy
- Post-assessment of a failed or delayed initiative to understand what assumptions proved wrong and why

## Skip If (ANY kills it)

- Single-team backlog refinement — strategy basics is heavy-weight; a one-page problem statement is sufficient
- Purely experimental product discovery before any commitment — use lean-canvas or opportunity-solution-trees first
- Well-understood engineering refactors with no business state change — strategy basics framing produces noise
- Crisis response or incident remediation — use root-cause analysis and post-mortem instead
- Decisions dominated by a single hard constraint (regulatory deadline, cost ceiling) — filter on that constraint alone first

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
