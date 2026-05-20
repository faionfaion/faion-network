---
slug: stripe-webhook-handler-pattern
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Canonical payment-webhook recipe: signature verification, idempotency key, replay handling, dead-letter.
content_id: "dc2883ba79133fbc"
tags: [stripe-webhook-handler-pattern, dev, solo]
---

# Stripe Webhook Handler Pattern

## Summary

**One-sentence:** Canonical payment-webhook recipe: signature verification, idempotency key, replay handling, dead-letter.

**One-paragraph:** High-frequency task for solo SaaS builders + outsource e-commerce work. No methodology touches Stripe or webhooks specifically. Output: handler skeleton + verification + idempotency + DLQ.

## Applies If (ALL must hold)

- Stripe is the payment processor
- ≥1 webhook event consumed (e.g., checkout.session.completed, invoice.paid)
- handler runs in a deployable service

## Skip If (ANY kills it)

- non-Stripe payment processor (use processor-specific guide)
- no webhooks (polling-only) — different pattern
- fully managed Stripe-hosted (e.g., Payment Links only)

## Prerequisites

- Stripe account with webhook endpoint configured
- webhook secret in secret manager
- queue or dead-letter for failed webhook processing

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/api-developer` | peer methodology — produces inputs or consumes outputs |
| `free/dev/backend-developer` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/dev/software-developer/`
- peer methodology: `solo/dev/api-developer`
- peer methodology: `free/dev/backend-developer`
- peer methodology: `pro/dev/stripe-webhook-handler-pattern`
- external: https://docs.stripe.com/webhooks; https://docs.stripe.com/payments/checkout/webhooks
