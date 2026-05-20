---
slug: ads-meta-reporting
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured analyze-decide-act cycle for Meta Ads: set up custom column presets (CPM, CTR, CPC, CVR, CPA, ROAS), run weekly breakdowns by age/placement/device, and diagnose performance issues by mapping symptoms (high CPA, low CTR, high frequency) to root causes (creative fatigue, audience fatigue, landing page failure).
content_id: "44b6aa8880385d87"
tags: [meta-ads, reporting, performance-analysis, diagnostics, cpa-optimization]
---
# Meta Ads Reporting & Analysis

## Summary

**One-sentence:** Structured analyze-decide-act cycle for Meta Ads: set up custom column presets (CPM, CTR, CPC, CVR, CPA, ROAS), run weekly breakdowns by age/placement/device, and diagnose performance issues by mapping symptoms (high CPA, low CTR, high frequency) to root causes (creative fatigue, audience fatigue, landing page failure).

**One-paragraph:** Structured analyze-decide-act cycle for Meta Ads: set up custom column presets (CPM, CTR, CPC, CVR, CPA, ROAS), run weekly breakdowns by age/placement/device, and diagnose performance issues by mapping symptoms (high CPA, low CTR, high frequency) to root causes (creative fatigue, audience fatigue, landing page failure). Every report must produce a list of concrete actions.

## Applies If (ALL must hold)

- Weekly performance review for any active Meta campaign.
- Diagnosing a CPA spike or CTR decline.
- Presenting results to stakeholders (executive summary, creative analysis).
- Deciding which campaigns to scale, hold, or pause.

## Skip If (ANY kills it)

- Daily micro-optimization — too noisy; check spend pacing and errors daily, but full analysis weekly.
- Campaigns in learning phase (less than 50 conversions in the optimization window) — data is not representative.
- Attribution decisions that require cross-platform modeling — use dedicated attribution tools, not Meta-only data.

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

- parent skill: `pro/marketing/ppc-manager/`
