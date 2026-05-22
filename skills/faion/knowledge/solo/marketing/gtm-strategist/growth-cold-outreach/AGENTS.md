---
slug: growth-cold-outreach
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured approach for converting strangers into customers via targeted cold email and LinkedIn: build a focused prospect list, personalize using research, keep emails under 5 sentences, and follow up 4–5 times.
content_id: "00f5e1e5dd1a7fc4"
tags: [cold-email, outreach, sales, b2b, lead-generation]
---
# Cold Outreach

## Summary

**One-sentence:** A structured approach for converting strangers into customers via targeted cold email and LinkedIn: build a focused prospect list, personalize using research, keep emails under 5 sentences, and follow up 4–5 times.

**One-paragraph:** A structured approach for converting strangers into customers via targeted cold email and LinkedIn: build a focused prospect list, personalize using research, keep emails under 5 sentences, and follow up 4–5 times. Deliverability infrastructure (separate domain, SPF/DKIM/DMARC, warm-up) is a prerequisite — without it, emails never reach the inbox. Inbound marketing takes months; cold outreach can produce customers this week.

## Applies If (ALL must hold)

- Zero or small audience; need customers before inbound scales
- Targeting a specific niche (role + industry + company size) where lists are buildable
- B2B products or services where individual decision-makers can be identified
- Outreach to potential partners, collaborators, or press

## Skip If (ANY kills it)

- B2C consumer products — cold outreach doesn't scale to consumer segments
- Regulated industries with anti-spam laws that prohibit unsolicited commercial email (check GDPR, CAN-SPAM, CASL for jurisdiction)
- Low-ACV products where the CAC of manual outreach exceeds LTV
- When deliverability infrastructure is not set up — sending from primary domain risks blacklisting

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

- parent skill: `solo/marketing/gtm-strategist/`
