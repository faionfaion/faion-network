---
slug: agency-proposal-template-system
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d8cf907dc3763950"
summary: Tiered (good / better / best) anchored-pricing proposal template system for micro-agency founders converting inbound leads to signed retainers in 4-6 weeks.
tags: [proposal, agency, sales, tiered-pricing, sow, micro-agency, anchored-pricing]
---
# Agency Tiered-Proposal Template System

## Summary

**One-sentence:** Tiered (good / better / best) anchored-pricing proposal template system for micro-agency founders converting inbound leads to signed retainers in 4-6 weeks.

**One-paragraph:** Existing statement-of-work playbook covers SOW structure but not the proposal-as-conversion-tool pattern that agency founders use. Mechanism: every inbound lead receives a single document with 3 packages — Good (entry, lower margin), Better (the target, anchored by the others), Best (stretch, signals capability ceiling). Each package has fixed scope, fixed monthly fee, fixed deliverables, and a 6-month minimum commitment. Proposal sent within 48h of discovery call. Sales cycle 4-6 weeks: discovery → proposal → 2 clarification touchpoints → signature. Primary output: a proposal doc per lead + a signed retainer.

## Applies If (ALL must hold)

- micro-agency / consultancy doing inbound or referral lead flow
- proposing retainers in the $3k-$25k/month range (mid-market service)
- proposal length 3-6 pages — long enough to articulate value, short enough to read in 15 min
- you can decide pricing without a committee (you ARE the committee)
- inbound leads have done at least one discovery call

## Skip If (ANY kills it)

- one-shot project proposals — different shape, use a project SOW template
- enterprise procurement with required RFP format — use the client's template, not yours
- pre-discovery cold outreach — proposal without discovery is hope, not strategy
- you don't have a baseline rate / hourly — proposal needs underlying math you can defend
- product / SaaS sales — use SaaS pricing pages, not proposal docs

## Prerequisites (must be true before starting)

- discovery call notes (problem, success criteria, decision-maker, budget hint, timeline)
- your baseline rate per role + capacity availability
- 3 case study / outcome references that match the lead's domain
- a contract template ready to attach to the chosen tier
- a 48-hour proposal-send commitment in your sales workflow

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/retainer-conversion-script` | Adjacent motion when converting existing project clients |
| `pro/pm/project-manager/agency-pnl-tracker-template` | Source of margin floors used to set tier pricing |
| `pro/product/product-operations/account-health-scoring-model` | Post-sale operating model the proposal points to |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 3 tiers always, anchor tier wins, fixed scope per tier, 48h send, 6-month minimum | ~900 |
| `content/02-output-contract.xml` | essential | Proposal doc schema, tier-comparison table schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (custom-everything, vague deliverables, à la carte erosion, discount-before-ask, missing exit ramp, proposal as feature dump) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tier_pricing_calc_from_discovery` | sonnet | Translate discovery notes + your rates into 3 anchored prices |
| `scope_per_tier_first_draft` | sonnet | Concrete deliverable list per package |
| `outcome_framing_synthesis` | opus | Lead's stated problem → outcome language across all 3 tiers |
| `proposal_letter_close` | sonnet | Personal closing paragraph referencing discovery specifics |

## Templates

| File | Purpose |
|------|---------|
| `templates/proposal-doc.md` | Full proposal template (problem / approach / 3 tiers / case studies / process / pricing / close) |
| `templates/tier-comparison-table.md` | The 3-tier comparison page with anchored pricing |
| `templates/discovery-to-proposal-checklist.md` | Steps from call → 48h send |
| `templates/proposal-cover-email.md` | Email that delivers the proposal with framing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/proposal-build-from-discovery.py` | Use discovery notes + rate sheet to bootstrap 3 tiers | Within 24h of discovery |
| `scripts/sanity-check-tier-math.py` | Verify each tier's price clears margin floor | Before sending |

## Related

- parent skill: `pro/marketing/gtm-strategist/`
- peer methodologies: `retainer-conversion-script`, `agency-pnl-tracker-template`, `growth-gtm-strategy`
- external: [Blair Enns - Win Without Pitching Manifesto](https://www.winwithoutpitching.com/) · [Jonathan Stark - Pricing Creativity](https://jonathanstark.com/) · [Mike Monteiro - Design Is a Job](https://abookapart.com/products/design-is-a-job)
