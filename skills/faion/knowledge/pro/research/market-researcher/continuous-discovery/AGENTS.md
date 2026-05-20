---
slug: continuous-discovery
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Continuous discovery is the practice of running weekly market-scanning and competitor-monitoring loops instead of one-shot research sprints.
content_id: "09d2bd7b60d51b4e"
tags: [competitive-intelligence, market-scanning, competitor-monitoring, continuous-research, pricing-intelligence]
---
# Continuous Discovery

## Summary

**One-sentence:** Continuous discovery is the practice of running weekly market-scanning and competitor-monitoring loops instead of one-shot research sprints.

**One-paragraph:** Continuous discovery is the practice of running weekly market-scanning and competitor-monitoring loops instead of one-shot research sprints. Rather than treating market intelligence as a project-start deliverable, it maintains a living picture of competitors, pricing, new entrants, and category signals on a daily/weekly/bi-weekly cadence using cheap models for data collection and Opus only for synthesis.

## Applies If (ALL must hold)

- Live category where competitors ship weekly and a 6-month-old market map is already wrong.
- Pricing-sensitive segments where competitor packaging changes erode conversion within days.
- GTM teams needing a weekly "what changed" digest without burning a senior analyst.
- Funded categories where new entrants (YC batches, ProductHunt launches) appear faster than a quarterly TAM refresh catches.
- Geo expansion plays where local competitors and regulatory shifts move the SOM monthly.
- Post-launch defense: detecting when a fast-follower clones your wedge before churn shows up.
- A live category where competitors ship weekly (AI tooling, dev tools, fintech, creator SaaS) and a 6-month-old market map is already wrong.
- Pricing-sensitive segments (PLG SaaS, marketplaces) where competitor price/packaging changes erode conversion within days.
- Funded categories where new entrants (YC batches, ProductHunt launches, Stripe Atlas filings) appear faster than a quarterly TAM refresh can catch.
- Geo expansion plays where local competitors and regulatory shifts (DSA, EU AI Act, state-level US privacy) materially move the SOM monthly.
- Solopreneur stacks operating like a one-person research firm — the only way to keep a monitoring matrix alive is via cron + agents.
- Post-launch defense: detecting the moment a fast-follower clones your wedge, before churn shows up in the funnel.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with no defined competitive set — run competitor-analysis once first.
- Slow-moving regulated categories (medtech, defense, classical banking) where half-life is years.
- Compliance-bound enterprise sales with 12-18 month cycles — quarterly snapshots beat noisy weekly diffs.
- Single-customer custom-software work — no "market" to scan.
- When the team will not act on signals — unread scans become a research graveyard that burns tokens.
- Crisis mode (active outage, churn cliff) — pause scan, focus on incident, resume after stabilization.
- Pre-PMF zero-to-one with no defined competitive set — start with market-research-tam-sam-som and competitor-analysis once, not a rolling scan.
- Slow-moving regulated categories (medtech devices, defense, classical banking) where the market half-life is measured in years.
- Compliance-bound enterprise sales with 12–18 month cycles — quarterly market snapshots beat noisy weekly diffs.
- Single-customer custom-software work — there is no "market" to scan; switch to account-level intelligence.
- When the team will not act on signals — a continuously scanned market that nobody reads becomes a research graveyard and burns tokens.
- Crisis mode (active outage, churn cliff, lawsuit) — pause the scan, focus humans on the incident, resume after stabilization.

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

- parent skill: `pro/research/market-researcher/`
