---
slug: ads-ab-testing-ads
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Scientific method applied to ad creative: pre-register one hypothesis (one variable changed), calculate required sample size before launching, run control vs.
content_id: "9c72256f0d117d61"
tags: [a-b-testing, ppc, ads, experimentation, statistics]
---
# A/B Testing Ads

## Summary

**One-sentence:** Scientific method applied to ad creative: pre-register one hypothesis (one variable changed), calculate required sample size before launching, run control vs.

**One-paragraph:** Scientific method applied to ad creative: pre-register one hypothesis (one variable changed), calculate required sample size before launching, run control vs. variant on the same audience with equal budget, and only verdict once 95% confidence is reached. Test in priority order: offer → hook/headline → creative type → visual style → copy length → CTA. Document every result to build an institutional learning library.

## Applies If (ALL must hold)

- Running a continuous testing cadence across hooks, creatives, and offers.
- Evaluating a specific creative hypothesis before scaling spend.
- Coordinating cross-platform tests (Meta + Google) on the same hypothesis.
- Maintaining a tests registry for team knowledge sharing.

## Skip If (ANY kills it)

- Daily/weekly conversion volume below 100 per variant — tests will never reach significance; ship the better-reasoned option and move on.
- Brand-new accounts with under 30 days history — algorithmic variance dominates creative variance.
- Holiday peaks (BFCM, Q4 retail) — exogenous demand swamps treatment effect; run proven creatives.
- Tests where multiple variables changed — use multivariate or Bandit design instead.

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
