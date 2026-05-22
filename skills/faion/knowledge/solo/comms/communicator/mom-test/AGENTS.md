---
slug: mom-test
tier: solo
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Mom Test (Rob Fitzpatrick, 2013) is a customer discovery interview protocol with three rules: talk about their life not your idea; ask about past specifics not future hypotheticals; talk less than 20% of the time.
content_id: "4da4a39e8096794f"
tags: [mom-test, customer-discovery, validation, interviews, product-research]
---
# The Mom Test: Customer Discovery Interview Protocol

## Summary

**One-sentence:** The Mom Test (Rob Fitzpatrick, 2013) is a customer discovery interview protocol with three rules: talk about their life not your idea; ask about past specifics not future hypotheticals; talk less than 20% of the time.

**One-paragraph:** The Mom Test (Rob Fitzpatrick, 2013) is a customer discovery interview protocol with three rules: talk about their life not your idea; ask about past specifics not future hypotheticals; talk less than 20% of the time. It distinguishes genuine problem signals (specific past behavior, current spending, commitments) from worthless compliments ("sounds cool", "I would use this"). Real validation requires commitment — time (beta test), reputation (referral), or money (deposit) — not verbal enthusiasm.

## Applies If (ALL must hold)

- Early customer discovery before any code is written — validating that a problem is real and frequent.
- Screening interview transcripts to identify genuine signals vs polite noise.
- Generating interview question scripts that avoid leading, future-hypothetical, or opinion-seeking phrasing.
- Extracting commitment signals (time, money, referrals) from existing interview notes or CRM records.
- After 5+ interviews, running a synthesis pass to surface repeated patterns.

## Skip If (ANY kills it)

- Post-launch product analytics — Mom Test is a discovery tool, not a measurement tool.
- B2B enterprise procurement where formal RFPs are required — conversational style reads as unprepared.
- Quantitative surveys — explicitly qualitative, single-subject methodology.
- When you already have paying customers with observable behavior; switch to churn/retention analysis.

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

- parent skill: `solo/comms/communicator/`
