---
slug: solo-testimonial-extraction-script
tier: solo
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "268c5d2a28b8f42c"
summary: A 3-question testimonial elicitation script that produces a usable quote, a metric, and a use-case sentence in one customer reply — replacing "could you write us a testimonial?" with a high-yield interview pattern.
tags: [testimonials, social-proof, customer-comms, freelance, marketing]
---

# Solo Testimonial Extraction Script

## Summary

**One-sentence:** A 3-question testimonial elicitation script that produces a usable quote, a metric, and a use-case sentence in one customer reply — replacing "could you write us a testimonial?" with a high-yield interview pattern.

**One-paragraph:** Sean D'Souza ("The Brain Audit") and Joanna Wiebe (Copyhackers) documented a 3-question structure that flips testimonial extraction from "write something nice" to a guided interview: (1) what was the hesitation before buying, (2) what happened that made it worth it, (3) who would you NOT recommend this to. The third question disarms generic praise and produces specific, credible language. This methodology codifies the script, the send template, and the structured output schema. Output: `Testimonial` JSON with hesitation, outcome, anti-recommendation, and a 90-day follow-up reminder.

## Applies If (ALL must hold)

- engagement just closed (≤ 14 days since handover) OR customer hit a measurable milestone
- customer has been billed and paid (no testimonials from free / trial users)
- customer is reachable by email or DM (no LinkedIn ghosting)
- operator needs case-study or social-proof content this quarter

## Skip If (ANY kills it)

- engagement was rocky or NPS &lt; 7 — pulling a testimonial here forces a lie
- customer is bound by NDA / corporate gag — request named-anonymous case study instead
- customer asked NOT to be public — respect immediately
- it has been &gt; 90 days since the milestone — memory decay (per JTBD r4 logic)

## Prerequisites

- specific outcome the engagement produced (revenue, time saved, bug fixed) with a number
- relationship history (first name, prior thread, last touchpoint)
- operator's case-study template that consumes the output

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/testimonial-harvest-sop` | Sister SOP: end-of-engagement harvest workflow that calls this script |
| `pro/research/researcher/jobs-to-be-done` | Reuses the switcher-recency rule for memory freshness |
| `pro/marketing/growth-marketer/case-study-anatomy` | Downstream consumer of the structured testimonial |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 3-question structure, anti-recommend disarming, verbatim, consent, no-edit | ~900 |
| `content/02-output-contract.xml` | essential | `Testimonial` schema + consent flag + display variants | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: generic praise, AI-rewrite, missing metric, no consent | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `outreach_message_draft` | haiku | Template fill |
| `response_parse` | sonnet | Quote extraction with bounded judgment |
| `display_variants_compose` | sonnet | 3 lengths (full, mid, short) |
| `consent_verification` | sonnet | Check for explicit consent token |

## Templates

| File | Purpose |
|------|---------|
| `templates/outreach-email.md` | The 3-question email |
| `templates/testimonial.json` | Output schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/send-3q-outreach.py` | Sends the script email and stores response | Engagement closure trigger |

## Related

- parent skill: `solo/comms/communicator/`
- peer methodologies: `testimonial-harvest-sop`, `case-study-anatomy`
- external: [Sean D'Souza — The Brain Audit (PsychoTactics)](https://www.psychotactics.com/brain-audit-book/) · [Joanna Wiebe — Copyhackers testimonial post](https://copyhackers.com/2020/09/customer-testimonial-questions/) · [Casey Hill — testimonial elicitation](https://www.linkedin.com/in/caseyhill/)
