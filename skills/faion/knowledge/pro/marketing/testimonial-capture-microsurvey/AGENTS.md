---
slug: testimonial-capture-microsurvey
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ccd5fac359978b1d"
summary: "Testimonial Capture Microsurvey: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture'."
tags: [testimonial-capture-microsurvey, marketing, pro]
---
# Testimonial Capture Microsurvey

## Summary

**One-sentence:** Testimonial Capture Microsurvey: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture': growth-customer-testimonials is high-level; a 3-question microsurvey template + permission flow is the actual atomic task. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a testimonial capture microsurvey artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working testimonial capture microsurvey artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Testimonial Capture Microsurvey |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/testimonial-capture-microsurvey.json` | JSON schema for the Testimonial Capture Microsurvey output contract |
| `templates/testimonial-capture-microsurvey.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testimonial-capture-microsurvey.py` | Enforce Testimonial Capture Microsurvey output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `p5-micro-agency-founder/Bi-weekly case-study / testimonial capture`
- pro/marketing/p5-micro-agency-founder
