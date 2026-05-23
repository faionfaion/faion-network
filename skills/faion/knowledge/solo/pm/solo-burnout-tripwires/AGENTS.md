---
slug: solo-burnout-tripwires
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
content_id: "242fd1008d1fe251"
summary: Six quantitative burnout-early-warning tripwires (sleep, weekend creep, MRR-to-effort, joy channel, health-deferral, social contact) the solo founder configures once and reviews in two minutes weekly.
complexity: light
produces: checklist
est_tokens: 3200
tags: [burnout, solo, tripwires, wellbeing]
---
# Solo Burnout Tripwires

## Summary

**One-sentence:** A set of six quantitative tripwires the solo founder configures once, then reviews weekly — designed to fire well before subjective burnout, when remediation is still cheap.

**One-paragraph:** Roadmap-for-one-person methodologies talk about cadence; founder operating systems talk about focus. Neither defines the early-warning signals that say "you are about to burn out." This methodology specifies six quantitative tripwires — sleep duration, weekend-work creep, MRR-to-hours ratio, joy-channel presence, doctor/dentist deferral count, social-contact frequency — each with a threshold and a one-step response. Setup is once; the weekly review is two minutes.

**Ефективно для:**

- Solo founder operating without a co-founder safety net.
- Founder full-time on a live product, post-revenue or post-launch.
- Replacing "I'll rest after launch" with a measurable brake.
- Catching the burnout curve 6-8 weeks before subjective collapse.

## Applies If (ALL must hold)

- Solo founder operating without a co-founder or team safety net.
- Product is live and revenue-generating OR the founder is full-time on it.
- Founder can self-track sleep + calendar (any tracker — phone, watch, paper).
- Weekly review block exists in the calendar.

## Skip If (ANY kills it)

- Hobby project on the side, day-job pays the bills — burnout risk surface is different.
- Acute crisis week (launch, fundraise, family) — defer review for one week.
- Founder is already in clinical burnout — this is prevention, not treatment; seek a professional.
- No tracking instrument at all — defer until any tracker exists.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sleep tracker (Apple Health, Whoop, Oura, or manual log) | app | founder |
| Calendar access for weekend-work detection | calendar | founder |
| MRR dashboard or last-month figure | dashboard | founder |
| Two-minute weekly review block | calendar | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[side-project-financial-runway]] | Financial pressure is the most common burnout amplifier; runway anchors the MRR-to-effort tripwire. |
| [[solo-context-switch-protocol]] | Mode-batching protocol controls weekend-work creep at the day level. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: sleep, weekend creep, MRR/effort, joy channel, health-deferral, social contact | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for weekly tripwire-review checklist + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: un-anchored review, deferred-until-after-launch, single-tripwire-only | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `weekly_review_compose` | haiku | 6 threshold checks; mechanical. |
| `verdict_decide` | sonnet | Per-week judgement on "act vs continue". |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-review.yaml` | Per-week tripwire checklist skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-burnout-tripwires.py` | Validate weekly review against 02-output-contract schema | Weekly review block |

## Related

- [[side-project-financial-runway]]
- [[solo-context-switch-protocol]]
- [[solo-time-tracking-discipline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by which tripwires are red onto a rule from `content/01-core-rules.xml`, telling the founder whether to continue, act on a specific signal, or block new feature work. Walk it every Sunday or Monday in the two-minute slot.
