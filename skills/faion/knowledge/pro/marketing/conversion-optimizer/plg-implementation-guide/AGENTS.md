---
slug: plg-implementation-guide
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A 5-phase sequential implementation roadmap for operationalizing a PLG model: (1) Foundation — define Aha moment and measure TTV; (2) Free Tier Design — limits, upgrade triggers, self-serve checkout; (3) Activation Optimization — onboarding, templates, TTV under 5 minutes; (4) Monetization — PQL scoring, upgrade prompts, automated playbooks; (5) Expansion — seat/usage triggers, expansion revenue tracking.
content_id: "d9778169460cfeb6"
tags: [plg, implementation, playbooks, aha-moment, pql]
---
# PLG Implementation Guide

## Summary

**One-sentence:** A 5-phase sequential implementation roadmap for operationalizing a PLG model: (1) Foundation — define Aha moment and measure TTV; (2) Free Tier Design — limits, upgrade triggers, self-serve checkout; (3) Activation Optimization — onboarding, templates, TTV under 5 minutes; (4) Monetization — PQL scoring, upgrade prompts, automated playbooks; (5) Expansion — seat/usage triggers, expansion revenue tracking.

**One-paragraph:** A 5-phase sequential implementation roadmap for operationalizing a PLG model: (1) Foundation — define Aha moment and measure TTV; (2) Free Tier Design — limits, upgrade triggers, self-serve checkout; (3) Activation Optimization — onboarding, templates, TTV under 5 minutes; (4) Monetization — PQL scoring, upgrade prompts, automated playbooks; (5) Expansion — seat/usage triggers, expansion revenue tracking. Run phases in order — each depends on prior instrumentation.

## Applies If (ALL must hold)

- Operationalizing a PLG model after plg-basics selected one.
- Producing a phased rollout plan that maps to engineering tickets.
- Running freemium-to-paid, trial-to-paid, or expansion playbooks as deterministic Day-N sequences.
- Selecting and justifying the PLG tech stack (analytics, onboarding, billing, PQL scoring).

## Skip If (ANY kills it)

- High-level PLG model choice — route to plg-basics.
- Stage-specific tactic catalog — route to plg-optimization-tactics.
- Metric definitions and PQL math — route to plg-metrics.
- Pre-PMF teams without an Aha-moment hypothesis — running this checklist before PMF wastes engineering cycles.

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

- parent skill: `pro/marketing/conversion-optimizer/`
