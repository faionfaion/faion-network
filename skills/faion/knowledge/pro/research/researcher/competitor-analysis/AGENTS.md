---
slug: competitor-analysis
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A 5-step framework for systematically studying businesses competing for the same customers: identify (direct / indirect / future), map on a positioning matrix, analyse across 8 dimensions, find gaps, then define differentiation.
content_id: "8400614a49ae87f5"
tags: [competitor-analysis, positioning, market-research, differentiation, gap-analysis]
---
# Competitor Analysis

## Summary

**One-sentence:** A 5-step framework for systematically studying businesses competing for the same customers: identify (direct / indirect / future), map on a positioning matrix, analyse across 8 dimensions, find gaps, then define differentiation.

**One-paragraph:** A 5-step framework for systematically studying businesses competing for the same customers: identify (direct / indirect / future), map on a positioning matrix, analyse across 8 dimensions, find gaps, then define differentiation. Output is competitive-analysis.md in .aidocs/product_docs/.

## Applies If (ALL must hold)

- Pre-MVP: 5-10 candidate competitors identified, need structured scan before committing engineering time.
- Positioning sprint: landing page or pricing rewrite requiring a defensible differentiation statement.
- New feature greenlight: comparing how 3-7 incumbents implement a feature you plan to build.
- Quarterly market refresh: re-scoring known competitors on price, features, and traction.
- Investor / pitch deck: building a credible competitor matrix slide with named gaps.

## Skip If (ANY kills it)

- Deep customer-pain discovery—competitors are a proxy, not a substitute for user interviews; use pain-points or problem-validation first.
- Pure brainstorming with no category defined yet—run idea-generation-methods first.
- Regulated / B2B-enterprise procurement where pricing is hidden behind sales—agents will hallucinate numbers.
- Real-time monitoring of a single competitor—use a change-tracking service (Visualping), not a one-shot agent run.
- "Should we build this?" gut checks—competitor count alone does not answer that.

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

- parent skill: `pro/research/researcher/`
