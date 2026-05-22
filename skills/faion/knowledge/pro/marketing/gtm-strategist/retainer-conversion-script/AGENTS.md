---
slug: retainer-conversion-script
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3ae940f89a0b50ed"
summary: Converts a one-shot project client into a recurring retainer through a 3-touchpoint script during the final 4 weeks of the engagement.
tags: [retainer, conversion, service-business, micro-agency, freelance, recurring-revenue]
---
# Project-to-Retainer Conversion Script

## Summary

**One-sentence:** Converts a one-shot project client into a recurring retainer through a 3-touchpoint script during the final 4 weeks of the engagement.

**One-paragraph:** Existing SaaS upsell methodology assumes product-led mechanics; this is the service-business motion. Mechanism: at project week N-4, plant the seed ("here's what would atrophy without ongoing attention"); at N-2, propose 3-tiered retainer with anchor pricing (good/better/best); at N (handoff), close on the named option. Each touchpoint has verbatim language, sequencing, and exit gates. The goal is not to convince — it's to surface clients who actually have ongoing need, before they drift to a different vendor by default. Primary output: signed retainer contract OR clean "no" with a referral ask.

## Applies If (ALL must hold)

- you operate a service business (agency, consultancy, freelance) doing project-based work
- current client engagement is within 4 weeks of contracted end date
- the work has ongoing maintenance / iteration value (not a one-shot delivery like a logo)
- client is the same decision-maker who signed the original project SOW
- you have capacity to take on the retainer (60-80% utilization or below)

## Skip If (ANY kills it)

- pure one-shot delivery (legal contract draft, single-fix bug) — no ongoing need exists
- client is a hostile-handoff or strained relationship — retainer compounds friction
- you're at &gt;90% capacity — taking the retainer means failing existing clients
- client already has internal team for the ongoing work — your retainer would be duplicate
- SaaS product company doing seat-based upsell — use SaaS upsell methodology

## Prerequisites (must be true before starting)

- project SOW with named deliverables, end date, and total $ value
- record of mid-project value moments (something that went well that client praised)
- a "what would atrophy without us" list — 3-5 concrete things the client will need someone to do
- proposed retainer pricing in 3 tiers: low (40-60% of project monthly equivalent), medium, high
- contract template for the retainer (signed-off SOW skeleton) ready to send

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/agency-proposal-template-system` | Provides the good/better/best tiered proposal template used at touchpoint 2 |
| `pro/pm/project-manager/quarterly-retainer-review-script` | Sets expectations for the post-conversion review cadence |
| `pro/marketing/gtm-strategist/ops-upselling-cross-selling` | Adjacent motion for clients already on a retainer scaling up |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 3-touchpoint cadence, anchor on atrophy not benefits, tiered offer, clean-no allowed, no discount in first conversation | ~900 |
| `content/02-output-contract.xml` | essential | Touchpoint message schemas, decision-record schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (premature pitch, feature dump, discount panic, ghost outcome, vague scope, capacity collision) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `atrophy_list_draft` | sonnet | Cross-deliverable reasoning, bounded scope |
| `touchpoint_message_draft` | sonnet | Persuasion structure with templated language |
| `tier_pricing_anchor_synthesis` | opus | Cross-input judgment (project value + client size + your capacity) |
| `clean_no_response_draft` | haiku | Template fill: gratitude + referral ask |

## Templates

| File | Purpose |
|------|---------|
| `templates/touchpoint-1-seed.md` | Week N-4 message planting the atrophy frame |
| `templates/touchpoint-2-proposal.md` | Week N-2 3-tier proposal with verbatim opener |
| `templates/touchpoint-3-close.md` | Handoff week close conversation script |
| `templates/clean-no-followup.md` | Post-no response with referral ask |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/atrophy-list-generator.py` | Generate the 3-5 "without us" items from project deliverable list | Before touchpoint 1 |
| `scripts/tier-pricing-calculator.py` | Compute 3-tier retainer pricing from project $ + client size + your hourly | Before touchpoint 2 |

## Related

- parent skill: `pro/marketing/gtm-strategist/`
- peer methodologies: `agency-proposal-template-system`, `quarterly-retainer-review-script`, `account-health-scoring-model`
- external: [Blair Enns - Win Without Pitching](https://www.winwithoutpitching.com/) · [Jonathan Stark - Pricing Creativity](https://jonathanstark.com/) · [HBR - Recurring Revenue](https://hbr.org/2016/01/the-future-of-saas-pricing)
