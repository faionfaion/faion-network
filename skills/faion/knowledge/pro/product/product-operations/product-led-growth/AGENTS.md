# Product-Led Growth (PLG)

## Summary

PLG uses the product itself as the primary acquisition, activation, and expansion engine: self-serve onboarding, a clearly defined "aha moment" under 5 minutes, usage-gated upgrade triggers, and PQL scoring that hands off to sales-assist at the right moment. The agent workflow instruments the funnel, generates activation hypotheses, ships the smallest in-product change behind a feature flag, and gates experimentation behind SRM check and pre-registered MDE.

## Why

Traditional sales-led growth economics break down below ~$25k ACV — the cost per SDR exceeds the contract value. PLG companies achieve higher revenue per employee (Ahrefs reached $40M ARR with 40 people) because the product itself drives the conversion loop. Without instrumentation-first discipline, agents optimise on uninstrumented funnels and hill-climb noise; without a usage-gate in the free tier, there is no upgrade trigger.

## When To Use

- SaaS / dev tools / API products where users can self-onboard without sales (Linear, Vercel, PostHog pattern).
- ACV under ~$25k where sales-led economics break down; freemium → paid conversion is the growth lever.
- Product produces measurable in-app events (signup, activation step, feature use) that can drive PQL scoring.
- Bottom-up motion targeting individual contributors who later expand to teams (Slack, Notion, Figma pattern).
- Existing product with traffic but flat activation — room for funnel instrumentation and onboarding redesign.

## When NOT To Use

- Highly regulated, procurement-heavy enterprise sales (defense, banking core) — buyer is not the user.
- Products requiring data integration, on-prem deploy, or contracts before any value can be shown.
- ACV above ~$100k where one closed deal pays for many SDRs; sales-led ROI dominates.
- Pre-PMF: PLG amplifies a working loop; on a broken product it industrialises churn.
- Network products without single-player value — optimising activation has no payoff if the user lands alone.

## Content

| File | What's inside |
|------|---------------|
| `content/01-plg-principles.xml` | Four core principles, key metrics (activation rate, TTV, PQL, expansion revenue rate, NRR) with 2026 targets, PLG evolution notes |
| `content/02-onboarding-and-experiments.xml` | Onboarding best practices, experiment design rules (SRM, MDE, minimum exposure), PQL scoring pattern, hybrid PLG+sales-assist |
| `content/03-rules-and-gotchas.xml` | Instrumentation-first rule, usage-gate rule, persona-segmentation rule, agent gotchas (over-fit, metric invention, tour-builder adding steps) |

## Templates

| File | Purpose |
|------|---------|
| `templates/pql-scorer.py` | PostHog-based PQL scorer: weight in-app events, write pql_score + pql_tier back as person properties |
