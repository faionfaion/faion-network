---
slug: govtech-foia-ba-pack
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: FOIA / records-retention requirements, WCAG AA, Section 508 / EN 301 549, procurement constraints — the vertical BA pack public-sector engagements need.
content_id: "afff0192d0d4d5ba"
tags: [govtech-foia-ba-pack, ba, geek]
---

# GovTech FOIA / Records-Retention BA Pack

## Summary

**One-sentence:** FOIA / records-retention requirements, WCAG AA, Section 508 / EN 301 549, procurement constraints — the vertical BA pack public-sector engagements need.

**One-paragraph:** GovTech / public-sector engagements need FOIA / records-retention, accessibility, Section 508 / EN 301 549, procurement constraints. Outsource teams pitch this work without methodology backing. Output: gov requirements template + accessibility checklist + procurement checklist.

## Applies If (ALL must hold)

- BA on a government / public-sector engagement
- scope includes records retention, FOIA, accessibility, or procurement
- client jurisdiction is identifiable (US federal/state, UK, EU member, Canada)

## Skip If (ANY kills it)

- private-sector with no public-records obligation
- purely informational static site (no transactions)
- compliance handled by separate audit firm — defer to them

## Prerequisites

- jurisdiction + applicable laws list
- client's existing records-retention schedule
- accessibility target level (AA default, AAA if pushed)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent skill — provides operating context for this methodology |
| `pro/ba/business-analyst` | peer methodology — produces inputs or consumes outputs |
| `pro/sec/data-classification` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `pro/ba/business-analyst`
- peer methodology: `pro/sec/data-classification`
- peer methodology: `pro/ux/accessibility-specialist`
- external: https://www.foia.gov/; https://www.section508.gov/; https://www.w3.org/WAI/standards-guidelines/wcag/
