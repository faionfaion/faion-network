---
slug: strategy-analysis
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four sequential KA-6 tasks — analyze current state, define future state, assess risks, define change strategy — each with a strict input/output contract.
content_id: "15de4933d244b3ac"
tags: [babok, strategy, ka6, business-analysis, change-strategy]
---
# Strategy Analysis — BABOK Knowledge Area 6

## Summary

**One-sentence:** Four sequential KA-6 tasks — analyze current state, define future state, assess risks, define change strategy — each with a strict input/output contract.

**One-paragraph:** Four sequential KA-6 tasks — analyze current state, define future state, assess risks, define change strategy — each with a strict input/output contract. Initiatives that start without a validated current-state analysis and a measurable future state produce change strategies disconnected from real gaps. A KA-6 router that checks artifact presence and freshness (no artifact older than 90 days) prevents silently stale strategy work from driving budget decisions.

## Applies If (ALL must hold)

- Onboarding a BA agent to BABOK KA-6 layout — canonical map a routing agent uses to pick a sub-task
- Audit or gap-check of strategy artifacts: cross-checking that all four KA-6 tasks were performed
- Generating BABOK-aligned task scaffolding before deeper requirements work begins
- Mapping legacy strategy documents into BABOK terminology for Jama, Polarion, or Modern Requirements ingestion
- Training prompt grounding when a custom agent must reason in BABOK terms

## Skip If (ANY kills it)

- A non-BABOK strategy framework is already in force (Wardley mapping, OKR-only, JTBD-driven) — do not retrofit KA-6 on top
- Single-team backlog refinement — KA-6 is heavyweight; a one-page problem statement is enough
- Pure product-discovery experiments before any commitment — use lean-canvas / opportunity-solution-trees first
- Engineering-only refactors with no business-state change — KA-6 business-need framing produces noise

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
