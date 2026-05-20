---
slug: testimonial-harvest-sop
tier: solo
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "420c0cfd196d72b4"
summary: End-of-engagement standard operating procedure that yields a written quote, a Loom video, and one outcome metric from every closed service engagement — built on the 3-question script with project-handover triggers.
tags: [testimonials, sop, freelance, case-study, social-proof]
---

# Testimonial Harvest SOP

## Summary

**One-sentence:** End-of-engagement standard operating procedure that yields a written quote, a Loom video, and one outcome metric from every closed service engagement — built on the 3-question script with project-handover triggers.

**One-paragraph:** Solo service operators typically ask for testimonials weeks or months after closure, when memory has decayed and the customer has moved on. This SOP wires testimonial harvest into the handover ritual itself: 3 trigger events (final deliverable shipped, invoice paid, 30-day check-in), 3 outputs per engagement (written quote, 60-90s Loom, one metric), and a kill criterion (no harvest after 90 days). Output: `HarvestRecord` for every closed engagement with consent flags, plus an aggregate dashboard. Built on top of `solo-testimonial-extraction-script` for the actual elicitation language.

## Applies If (ALL must hold)

- service engagement (freelance, consulting, agency) just closed OR will close within 14 days
- engagement value &gt; $1000 OR runtime &gt; 4 weeks (smaller is too low yield)
- customer relationship is healthy (NPS ≥ 7 OR no documented friction)
- operator has the bandwidth to do 3 outreach attempts within 30 days

## Skip If (ANY kills it)

- engagement was rocky (NPS &lt; 6) — pulling a testimonial forces a lie
- customer has an NDA forbidding public attribution — request named-anonymous instead
- product engagement (SaaS) — use product-flavoured testimonial methodology, not this service SOP
- &gt; 90 days since closure — memory decay; route to "old-customer outreach" SOP instead

## Prerequisites

- engagement records with paid date, deliverables, customer contact
- access to Loom / a video tool the customer can record into
- the 3-question script template loaded (`solo-testimonial-extraction-script`)
- a case-study page or carousel where output will land

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/comms/communicator/solo-testimonial-extraction-script` | Provides the 3-question elicitation language this SOP triggers |
| `pro/marketing/growth-marketer/case-study-anatomy` | Downstream consumer of harvested artifacts |
| `solo/marketing/conversion-optimizer/solo-lead-qualification-rubric` | Confirms NPS ≥ 7 / no-rocky gate before harvest fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 3 triggers, 3 outputs, kill at 90d, NPS gate, consent layering | ~900 |
| `content/02-output-contract.xml` | essential | `HarvestRecord` + per-artifact schemas with consent + display rights | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: forced ask, video pressure, metric fabrication, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `handover_trigger_check` | haiku | Filesystem / CRM scan |
| `outreach_compose` | sonnet | Template fill calling 3Q script |
| `loom_request_compose` | sonnet | Different ask, different language |
| `harvest_record_assemble` | sonnet | Aggregation with consent layering |

## Templates

| File | Purpose |
|------|---------|
| `templates/harvest-record.json` | Output schema |
| `templates/loom-request.md` | Video-request email template |
| `templates/metric-extraction-prompt.md` | Numeric-metric ask |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/trigger-on-handover.py` | Detects handover, fires 3Q outreach | Project-close webhook |
| `scripts/30day-followup.py` | Sends 30-day check-in / Loom request | Cron 30 days after close |

## Related

- parent skill: `solo/marketing/conversion-optimizer/`
- peer methodologies: `solo-testimonial-extraction-script`, `case-study-anatomy`
- external: [Sean D'Souza — Brain Audit](https://www.psychotactics.com/brain-audit-book/) · [Patrick Campbell — testimonial-as-funnel](https://www.profitwell.com/) · [Loom for SaaS / agencies](https://www.loom.com/use-case/agencies)
