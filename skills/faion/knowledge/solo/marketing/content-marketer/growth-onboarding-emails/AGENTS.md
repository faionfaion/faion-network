---
slug: growth-onboarding-emails
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Behavior-triggered email sequences that guide new users from signup to activation.
content_id: "a5fb2ccf38f007d9"
tags: [onboarding, behavioral-triggers, activation, user-retention, email-sequences]
---
# Onboarding Email Sequences

## Summary

**One-sentence:** Behavior-triggered email sequences that guide new users from signup to activation.

**One-paragraph:** Behavior-triggered email sequences that guide new users from signup to activation. Each email has one CTA, fires on a specific user action (or inaction), and routes stuck users through an escalation ladder. Behavioral triggers outperform time-based sequences by 15-40% in activation rate.

## Applies If (ALL must hold)

- SaaS or app with free trial / freemium model and measurable activation steps
- Onboarding activation rate below 50% with no behavioral trigger emails in place
- Redesigning an existing time-based sequence to add behavior-triggered branches
- New product launch where the first-week user journey has been mapped
- Product has an identifiable "aha moment" milestone (connect data, create project, invite teammate)

## Skip If (ANY kills it)

- Product analytics not set up — behavioral triggers require event tracking (Segment, Mixpanel); without data, only time-based sequences are possible
- Transactional product with no recurring engagement cycle (one-time purchase, no return)
- User base is extremely homogeneous with a single known path — a 3-email linear sequence may outperform complex branching
- No ESP with automation capability — Customer.io, ActiveCampaign, or Intercom required; basic Mailchimp is insufficient

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

- parent skill: `solo/marketing/content-marketer/`
