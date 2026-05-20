---
slug: agency-case-study-template
tier: pro
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3bf9d11167e6e723"
summary: Five-part case-study skeleton (Context, Problem, Approach, Outcome, Lessons) for freelancers and micro-agencies, with quantified outcomes and one verbatim client quote.
tags: [case-study, portfolio, freelancer, agency, proof-asset]
---

# Agency / Freelancer Case Study Template

## Summary

**One-sentence:** Five-part case-study skeleton (Context, Problem, Approach, Outcome, Lessons) for freelancers and micro-agencies, with quantified outcomes and one verbatim client quote.

**One-paragraph:** Standardizes the proof asset that converts portfolio visitors into sales calls. Mechanism: pin a single client engagement to a Context-Problem-Approach-Outcome-Lessons (CPAOL) frame, force a quantified primary outcome (revenue, time saved, conversion delta) and one verbatim client quote with attribution, and explicitly mark scope-of-engagement vs scope-of-team to avoid overclaiming. Primary output: a 600-1200 word case study suitable for portfolio sites, sales decks, and proposal appendices.

## Applies If (ALL must hold)

- engagement_status ∈ {complete, mid-engagement_with_outcome_visible}
- client_consent_to_publish == true (written, includes name/logo policy)
- ≥1 quantified outcome metric available (with baseline)
- author = solo freelancer OR micro-agency (1-10 people)

## Skip If (ANY kills it)

- NDA forbids identifying client AND outcome — output would be a generic blob; use a vertical-anonymized case instead
- engagement < 4 weeks — too thin for CPAOL; write a testimonial snippet instead
- enterprise / 100+ person agency — use a multi-author corporate case-study process, not this template
- no quantified baseline — outcome is unfalsifiable; collect baseline first or write a process-only writeup

## Prerequisites

- written client publish-consent covering name, logo, metric disclosure scope
- baseline metric snapshot (taken pre-engagement or reconstructed from analytics)
- 1-2 verbatim client quotes captured during or post-engagement (with role + first-name attribution)
- engagement timeline (start, key milestones, end) with dates

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/growth-customer-testimonials` | Sources verbatim client quotes used in the Outcome section |
| `pro/marketing/conversion-optimizer/funnel-tactics-basics` | Frames where the case study sits in the visitor → lead → call funnel |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: CPAOL structure, quantified outcome, verbatim quote, scope honesty, single-engagement focus | ~900 |
| `content/02-output-contract.xml` | essential | Case-study object schema, evidence requirements, forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 LLM/agent failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `consent_and_baseline_intake` | haiku | Form fill from operator-supplied facts |
| `cpaol_draft_per_engagement` | sonnet | Structured synthesis from engagement notes; bounded |
| `metric_phrasing_and_quote_selection` | sonnet | Judgment on which metric leads, which quote pulls |

## Templates

| File | Purpose |
|------|---------|

## Scripts

| File | Purpose |
|------|---------|

## Related

- parent skill: `pro/marketing/conversion-optimizer/SKILL.md`
- peer methodologies: `solo/marketing/content-marketer/growth-customer-testimonials`, `solo/marketing/content-marketer/growth-content-marketing`
- external: [Basecamp case studies](https://basecamp.com/customers) · [Paul Jarvis "Company of One" case study format] · [Brennan Dunn "Double Your Freelancing" proposal-appendix model](https://doubleyourfreelancing.com/)
