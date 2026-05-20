---
slug: indie-hacker-tax-and-legal-essentials
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: MoR vs direct invoicing, Estonia e-Residency, US LLC for non-residents, VAT MOSS — the pre-first-sale tax/legal checklist with zero faion coverage today.
content_id: "08be44ea203b95ac"
tags: [indie-hacker-tax-and-legal-essentials, pm, solo]
---

# Indie Hacker Tax and Legal Essentials

## Summary

**One-sentence:** MoR vs direct invoicing, Estonia e-Residency, US LLC for non-residents, VAT MOSS — the pre-first-sale tax/legal checklist with zero faion coverage today.

**One-paragraph:** Solo founders abroad face MoR vs direct invoicing, Estonia e-Residency, US LLC for non-residents, VAT MOSS. Zero faion coverage and a real blocker before first sale to EU. Output: decision artefact + entity choice + tax registration list. NOT LEGAL ADVICE — methodology directs to advisors.

## Applies If (ALL must hold)

- solo founder selling SaaS / digital products
- international customers (≥1 cross-border sale planned)
- founder has not yet locked entity structure

## Skip If (ANY kills it)

- domestic-only product (single country)
- founder already advised by tax counsel
- agency / service business (different tax shape)

## Prerequisites

- founder's country of residence + citizenship
- expected customer countries (top 5)
- expected first-year revenue estimate

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent skill — provides operating context for this methodology |
| `solo/marketing/freelance-tax-cashflow-basics` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/stripe-webhook-handler-pattern` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/pm/project-manager/`
- peer methodology: `solo/marketing/freelance-tax-cashflow-basics`
- peer methodology: `solo/dev/stripe-webhook-handler-pattern`
- external: https://e-resident.gov.ee/; https://www.stripe.com/atlas; https://lemonsqueezy.com/help/topics/merchant-of-record; https://paddle.com/blog/merchant-of-record
