---
slug: vendor-evaluation-scorecard
tier: geek
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Recurring atomic-task scorecard for new SaaS tool, observability platform, AI provider evaluation — the buyer-side complement of gtm-* pages.
content_id: "99510b38f9e48b5f"
tags: [vendor-evaluation-scorecard, product, geek]
---

# Vendor Evaluation Scorecard

## Summary

**One-sentence:** Recurring atomic-task scorecard for new SaaS tool, observability platform, AI provider evaluation — the buyer-side complement of gtm-* pages.

**One-paragraph:** Vendor evaluation (new SaaS, observability, AI provider) is a recurring atomic task. faion has gtm-* (seller-side) pages but nothing buyer-side. Output: scorecard template + scoring policy + decision record.

## Applies If (ALL must hold)

- team evaluating a tool or platform
- ≥2 candidates exist
- PM/EM has authority to pick

## Skip If (ANY kills it)

- single-candidate (only one viable vendor)
- auto-buy mandated by parent org or compliance
- evaluation already covered by vendor-eval-framework (use the bigger one)

## Prerequisites

- candidates list + initial criteria
- scoring rubric + weights
- trial / demo access for each candidate

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `geek/pm/vendor-eval-framework` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/library-evaluation-rubric` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `geek/pm/vendor-eval-framework`
- peer methodology: `solo/dev/library-evaluation-rubric`
- external: https://www.softwareadvice.com/buyers-guides; https://www.g2.com/categories
