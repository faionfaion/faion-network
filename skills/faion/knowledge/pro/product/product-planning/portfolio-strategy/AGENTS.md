---
slug: portfolio-strategy
tier: pro
group: product
domain: product-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Three Horizons portfolio model allocates engineering capacity across H1 (Core, 70%), H2 (Adjacent, 20%), and H3 (Transformational, 10%), with ratios adjustable to macro conditions (Growth 60/25/15, Stable 70/20/10, Recession 80/15/5).
content_id: "ad75f157f75350b1"
tags: [portfolio-strategy, three-horizons, allocation, product-strategy, roadmap]
---
# Portfolio Strategy (70/20/10)

## Summary

**One-sentence:** The Three Horizons portfolio model allocates engineering capacity across H1 (Core, 70%), H2 (Adjacent, 20%), and H3 (Transformational, 10%), with ratios adjustable to macro conditions (Growth 60/25/15, Stable 70/20/10, Recession 80/15/5).

**One-paragraph:** The Three Horizons portfolio model allocates engineering capacity across H1 (Core, 70%), H2 (Adjacent, 20%), and H3 (Transformational, 10%), with ratios adjustable to macro conditions (Growth 60/25/15, Stable 70/20/10, Recession 80/15/5). Every initiative is tagged H1/H2/H3 with a revenue-evidence string. Allocation tracks engineering cost (loaded $ or person-weeks), not ticket count. H3 bets ship with a pre-committed kill threshold. Re-classify quarterly.

## Applies If (ALL must hold)

- Annual/quarterly roadmap planning where multiple bets compete for the same engineering capacity
- Multi-product company or solopreneur with 3+ shipped products needing a defensible split
- Macro shock (recession signal, funding cut, churn spike) forcing re-allocation from H3/H2 to H1
- Investor/leadership update showing the portfolio is neither all moonshots nor all maintenance
- Backlog sizing: tag every initiative H1/H2/H3 and verify sum matches target ratios

## Skip If (ANY kills it)

- Single-product seed-stage startup with one bet — no portfolio yet; allocate 100% to PMF
- Pure services / agency revenue where there is no product backlog to allocate against
- Engineering-only resource planning (sprints, on-call, infra) — use capacity planning instead
- Sub-feature prioritization inside one product — RICE / WSJF / Kano are sharper at that grain
- Crisis quarters where survival demands 100% on one fire

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

- parent skill: `pro/product/product-planning/`
