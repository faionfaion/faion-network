---
slug: solo-lead-qualification-rubric
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "fc5c4fc1c0c6b35b"
summary: ICE-style qualification rubric tuned to solo freelance signals (budget clarity, decision authority on call, sane timeline, no scarring contractor history) that replaces BANT for one-person services.
tags: [lead-qualification, freelance, discovery-call, ice-score, pipeline]
---

# Solo Lead Qualification Rubric

## Summary

**One-sentence:** ICE-style qualification rubric tuned to solo freelance signals (budget clarity, decision authority on call, sane timeline, no scarring contractor history) that replaces BANT for one-person services.

**One-paragraph:** BANT (Budget / Authority / Need / Timeline) was authored for IBM in 1956 for B2B field sales with quota-loaded reps and multi-stakeholder enterprise deals — and HubSpot has retired it from their own playbook because the framework misfires on inbound modern SaaS, let alone on a solo freelancer's pipeline of warm cold-DMs. This methodology gives the solo operator a 4-dimensional score (`Budget-clarity`, `Decision-on-call`, `Timeline-realism`, `Contractor-trauma-history`) on a 1-5 scale, with a hard pass / soft pass / decline threshold at 14 / 10 / <10 of 20. Output: structured `QualifiedLead` JSON record per inbound, drop-decision before any unpaid discovery time is burned.

## Applies If (ALL must hold)

- engagement_type ∈ {one-off-project, retainer, fixed-price-statement-of-work}
- operator is solo (no business development / SDR seat)
- lead source is inbound (LinkedIn DM, email reply, referral) — NOT outbound cold-email blast
- prospect has had at least one reply exchange (1-line "interested" is not enough)

## Skip If (ANY kills it)

- this is a referral from a paying repeat client — referral signal dominates, qualify lightly
- prospect is a friend / personal network introduction — relationship rules, not framework rules
- engagement value < $500 — qualification cost exceeds project margin
- you have empty calendar this week — pragmatic acceptance threshold drops; rubric becomes advisory only

## Prerequisites

- one full DM / email thread or one 15-min reply ladder with the prospect
- written offer or service menu the prospect responded to (anchors "Budget-clarity")
- list of red-flag patterns from your last three failed projects (anchors "Contractor-trauma" detection)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/solo-rate-floor-calculator` | Provides the floor rate below which the rubric automatically marks `Budget-clarity = 1` |
| `solo/comms/communicator/solo-testimonial-extraction-script` | Sister methodology used post-engagement; qualified-lead score predicts testimonial harvest success |
| `pro/marketing/conversion-optimizer/lead-magnet-design` | Upstream — feeds the kind of inbound this rubric scores |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4-dimensional scoring rubric, threshold rules, and the rate-floor coupling rule | ~900 |
| `content/02-output-contract.xml` | essential | `QualifiedLead` JSON schema, required fields, forbidden patterns (e.g. score without evidence) | ~700 |
| `content/03-failure-modes.xml` | essential | 6 known scoring failures: optimism bias, single-signal scoring, hallucinated authority, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_signals_from_thread` | haiku | Quote extraction; mechanical |
| `score_per_dimension` | sonnet | Bounded judgment against rubric anchors |
| `compose_qualified_lead_record` | sonnet | Schema-bound output, no creative synthesis |
| `borderline_case_review` | opus | Pass/decline decision when total ∈ [9, 12] |

## Templates

| File | Purpose |
|------|---------|
| `templates/qualified-lead.json` | Output JSON Schema |
| `templates/discovery-thread-rubric.md` | Operator-side scoring sheet |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-lead.py` | Apply rubric to a transcript file → emit `QualifiedLead` JSON | After thread is closed, before deciding to book discovery call |

## Related

- parent skill: `solo/marketing/conversion-optimizer/`
- peer methodologies: `solo-rate-floor-calculator`, `solo-testimonial-extraction-script`
- external: [HubSpot — Why BANT Is Broken](https://blog.hubspot.com/sales/bant) · [Sean Ellis ICE scoring](https://growthhackers.com/articles/the-ice-score) · [Patrick McKenzie — Don't Call Yourself A Programmer (rate-floor logic)](https://www.kalzumeus.com/2011/10/28/dont-call-yourself-a-programmer/)
