---
slug: competitor-analysis
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Competitor analysis is the systematic study of businesses competing for the same customers, structured as a SWOT-grid + market-share estimation + portfolio scorecard workflow.
content_id: "8400614a49ae87f5"
tags: [competitor-analysis, swot, market-share, portfolio-scorecard, strategic-group]
---
# Competitor Analysis

## Summary

**One-sentence:** Competitor analysis is the systematic study of businesses competing for the same customers, structured as a SWOT-grid + market-share estimation + portfolio scorecard workflow.

**One-paragraph:** Competitor analysis is the systematic study of businesses competing for the same customers, structured as a SWOT-grid + market-share estimation + portfolio scorecard workflow. The market-researcher variant produces defensible board-ready artifacts — share in 5% buckets, per-SWOT-cell citation URLs, strategic-group maps with pre-committed axes — rather than feature-level positioning advice.

## Applies If (ALL must hold)

- Annual strategy review: scoring 8-15 named competitors on a SWOT grid as input to a board or strategy deck.
- Market-share estimation: producing defensible "X holds ~N% of category Y" claims from public proxies.
- Portfolio benchmarking: comparing a product line against 3-7 incumbents on a fixed quarterly scorecard.
- M&A or partnership shortlist: ranking acquisition targets by SWOT fit and relative strategic-group position.
- Investor due diligence: evidence-backed competitor matrix for a Series A/B deck.
- Win-loss debrief input: cross-referencing lost deals with competitor SWOT.

## Skip If (ANY kills it)

- Single-feature spec or pricing-page rewrite — use the researcher variant; SWOT/share is overkill.
- Pre-MVP idea triage with no named competitors — use idea-generation-methods or niche-evaluation first.
- Real-time competitive monitoring — SWOT is a snapshot; use Klue/Crayon for live tracking.
- Regulated/enterprise-only categories where market share is locked behind Gartner/IDC reports — agents will fabricate share numbers; buy the report.
- Hyperlocal markets (single city, single B2B niche under 50 buyers) — public proxies do not exist.

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

- parent skill: `pro/research/market-researcher/`
