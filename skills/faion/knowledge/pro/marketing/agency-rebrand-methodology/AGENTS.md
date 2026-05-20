---
slug: agency-rebrand-methodology
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Drives an agency rebrand (founder-name → company, narrowed niche, raised prices) with client comms, portfolio migration, SEO continuity, and contract addenda.
content_id: "6fb21bc479ec4e61"
tags: [agency-rebrand-methodology, marketing, pro]
---

# Agency Rebrand Methodology

## Summary

**One-sentence:** Drives an agency rebrand (founder-name → company, narrowed niche, raised prices) with client comms, portfolio migration, SEO continuity, and contract addenda.

**One-paragraph:** Founders typically rebrand 1-3 times during the 2-3 person phase. Rebrands trigger churn, broken backlinks, awkward amendments, and identity ambiguity. Mechanism: a 60-day plan with explicit client-comms cadence, 301-redirect map, contract addendum template, and post-rebrand audit. Output: a versioned transition record with all decisions cited.

## Applies If (ALL must hold)

- agency has an existing brand (founder name, legacy LLC, or first-product name)
- ≥3 active clients and ≥10 historical clients
- new positioning is decided (use agency-niche-positioning first)
- founder accepts 30-60 days of slowed delivery during transition

## Skip If (ANY kills it)

- agency <6 months old — iterate the brand instead of rebranding
- agency >20 people with brand team in place — use corporate-brand methodology
- rebrand driven purely by cosmetics (logo change) — out of scope; use brand-refresh

## Prerequisites

- decided new brand name, domain, trademark clear
- list of active client contracts with renewal dates
- current backlink profile from Ahrefs/SEMrush exported as CSV

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/agency-niche-positioning` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/rate-increase-notice-template` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/agency-niche-positioning`
- peer methodology: `pro/marketing/rate-increase-notice-template`
- external: https://www.gov.uk/government/publications/rebranding-checklist (UK gov rebrand checklist)
