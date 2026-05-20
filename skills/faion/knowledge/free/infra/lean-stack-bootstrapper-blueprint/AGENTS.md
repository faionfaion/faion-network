---
slug: lean-stack-bootstrapper-blueprint
tier: free
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Vercel + Supabase + Stripe + Cloudflare lean-stack reference at free tier — the tier-correct alternative to Docker/k8s overkill for indie hackers.
content_id: "23c9e2b094c1c544"
tags: [lean-stack-bootstrapper-blueprint, infra, free]
---

# Lean Stack Bootstrapper Blueprint

## Summary

**One-sentence:** Vercel + Supabase + Stripe + Cloudflare lean-stack reference at free tier — the tier-correct alternative to Docker/k8s overkill for indie hackers.

**One-paragraph:** faion infra knowledge skews to Docker/k8s/CI/CD heavy stacks (Pro). P2 reality: Vercel + Supabase + Stripe + Cloudflare. Need a tier-correct lean-stack at free tier. Output: stack diagram + cost ceiling + upgrade triggers.

## Applies If (ALL must hold)

- indie hacker building first 1-3 SaaS products
- <$5k/month budget for infra
- team size 1-2

## Skip If (ANY kills it)

- team ≥3 — graduate to opinionated infra (still solo tier)
- regulated data — lean stack vendors may not support compliance needs
- self-hosting requirement — different blueprint

## Prerequisites

- product type defined (web app, API, static + serverless)
- expected user count first 6 months
- stripe account or willingness to set up

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | parent skill — provides operating context for this methodology |
| `solo/infra/server-craft` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/supabase-mvp-stack` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/infra/server-craft/`
- peer methodology: `solo/infra/server-craft`
- peer methodology: `solo/dev/supabase-mvp-stack`
- peer methodology: `solo/dev/stripe-webhook-handler-pattern`
- external: https://vercel.com/docs; https://supabase.com/docs; https://stripe.com/docs; https://developers.cloudflare.com/
