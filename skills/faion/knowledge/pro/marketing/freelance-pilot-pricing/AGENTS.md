---
slug: freelance-pilot-pricing
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pilot / founder-price tactic for productized service first 3-5 customers — fixed scope, fixed price, 2-week timebox, public-case-study consent, post-pilot transition to standard price.
content_id: "freelance-pilot-1"
complexity: medium
produces: spec
est_tokens: 3200
tags: [freelance, pricing, pilot, productized, case-study]
---
# Freelance Pilot Pricing

## Summary

**One-sentence:** Pilot / founder-price tactic for productized service first 3-5 customers — fixed scope, fixed price, 2-week timebox, public-case-study consent, post-pilot transition to standard price.

**One-paragraph:** Generic pricing strategy doesn't cover the pilot/founder-price tactic that productized services rely on to land first 3-5 customers. This methodology pins the pilot shape: fixed scope, fixed price (50-70% of target), 2-week timebox max, consent to publish a public case study, and explicit transition language (post-pilot standard rate applies). Core rules: numeric price floor (never below cost basis); timebox ≤ 14 days; case-study consent captured in writing; transition price documented before pilot starts; pilot count capped at 5 customers before going standard.

**Ефективно для:**

- Productized service launching — first 3-5 customers.
- Niche pivot — establish proof points at the new price.
- Solo consultant — building case-study library.
- Agency niche launch — new offering needs anchor customers.

## Applies If (ALL must hold)

- Productized service (fixed-scope, repeatable offering).
- ≤5 pilot customers acquired to date for this specific offering.
- Authority to set price unilaterally (no committee approval).
- Capability to deliver in ≤14 days end-to-end.

## Skip If (ANY kills it)

- Mature offering with case studies + standard price established.
- Custom-bespoke project (each engagement different).
- Enterprise sale where 14-day pilot is implausible.
- Cost basis above target pilot price — losing money on pilots harms cashflow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cost basis per delivery | spreadsheet | own ops |
| Target standard price | spec | founder |
| Case-study consent template | doc | own ops |
| Pilot count to date | log | CRM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[fixed-vs-hourly-decision-framework]] | Pilot is a fixed shape — this is upstream context. |
| [[freelance-rate-jump-tactics]] | Standard price transition uses these tactics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: price-above-cost, timebox-14-days, case-study-consent-written, transition-price-documented, pilot-cap-5 | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-pilot-price` | haiku | Numeric arithmetic. |
| `draft-transition-clause` | sonnet | Light judgment on transition wording. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pilot-spec.json` | JSON example of one pilot spec |
| `templates/pilot-spec.md` | Markdown skeleton for pilot agreement appendix |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-pilot-pricing.py` | Validate one spec JSON against the schema | After draft, before publish |

## Related

- [[fixed-vs-hourly-decision-framework]]
- [[freelance-rate-jump-tactics]]
- [[freelancer-niche-positioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
