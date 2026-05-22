---
slug: audience-segmentation
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured process to divide a potential market into distinct, mutually exclusive groups using two to three differentiating dimensions (demographic, behavioural, psychographic, or needs-based), score each segment against six weighted attractiveness criteria, and select at most one primary target for pre-traction products.
content_id: "1b17d1bfb969be65"
tags: [segmentation, targeting, marketing-strategy, product-strategy, positioning]
---
# Audience Segmentation

## Summary

**One-sentence:** A structured process to divide a potential market into distinct, mutually exclusive groups using two to three differentiating dimensions (demographic, behavioural, psychographic, or needs-based), score each segment against six weighted attractiveness criteria, and select at most one primary target for pre-traction products.

**One-paragraph:** A structured process to divide a potential market into distinct, mutually exclusive groups using two to three differentiating dimensions (demographic, behavioural, psychographic, or needs-based), score each segment against six weighted attractiveness criteria, and select at most one primary target for pre-traction products. Segments are maintained as YAML/JSON for reproducible quarterly re-scoring.

## Applies If (ALL must hold)

- Pre-launch positioning when the team is debating which buyer to target first.
- Post-launch when "everyone is our customer" is eroding paid-acquisition efficiency.
- Pricing-tier design that needs distinct buying behaviours and willingness-to-pay levels.
- Pivoting into a new market where the prior segmentation no longer maps.
- Product-tier or product-line decisions (free/pro/enterprise; consumer/SMB/mid-market).

## Skip If (ANY kills it)

- Pre-traction MVPs with fewer than 50 customers — use one persona, not segment matrices.
- Strict niche businesses where the entire ICP fits one segment by design.
- Account-based sales motions where named accounts replace segmentation.
- Ephemeral campaigns — A/B-test creatives instead.

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

- parent skill: `pro/ux/user-researcher/`
