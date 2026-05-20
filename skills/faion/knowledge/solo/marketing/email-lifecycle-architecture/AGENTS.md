---
slug: email-lifecycle-architecture
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Acquisition → activation → engagement → retention → resurrection → churn lifecycle map with triggers, frequency caps, suppression rules, consent management — the system layer atomic email programs miss.
content_id: "208f1045f38e0080"
tags: [email-lifecycle-architecture, marketing, solo]
---

# Email Lifecycle Architecture

## Summary

**One-sentence:** Acquisition → activation → engagement → retention → resurrection → churn lifecycle map with triggers, frequency caps, suppression rules, consent management — the system layer atomic email programs miss.

**One-paragraph:** Faion has growth-email-marketing, growth-newsletter-growth, growth-onboarding-emails, customer-onboarding-email — all atomic. Nothing covers the lifecycle architecture: full map with triggers, frequency caps, suppression, consent spanning all email programs as one system. Output: lifecycle map + trigger inventory + frequency cap policy + consent record.

## Applies If (ALL must hold)

- ≥3 email programs running (welcome, newsletter, transactional, etc.)
- ≥1,000 subscribers OR ≥100 transactional emails/day
- founder/owner has authority to consolidate sender + suppression list

## Skip If (ANY kills it)

- single newsletter only — use growth-newsletter-growth
- transactional-only product (no marketing emails)
- regulated industry (HIPAA) — requires regulated-email patterns

## Prerequisites

- list of current email programs with sender + subscriber count
- current ESP(s) and segmentation capability
- consent + GDPR/CASL/CAN-SPAM compliance baseline

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer` | parent skill — provides operating context for this methodology |
| `solo/marketing/growth-email-marketing` | peer methodology — produces inputs or consumes outputs |
| `solo/marketing/growth-newsletter-growth` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/marketing/content-marketer/`
- peer methodology: `solo/marketing/growth-email-marketing`
- peer methodology: `solo/marketing/growth-newsletter-growth`
- peer methodology: `solo/marketing/growth-onboarding-emails`
- external: https://www.litmus.com/blog/email-marketing-lifecycle; https://gdpr.eu/article-7-conditions-for-consent/
