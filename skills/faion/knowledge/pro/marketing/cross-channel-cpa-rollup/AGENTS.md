---
slug: cross-channel-cpa-rollup
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8957490fb33045c7"
summary: A normalized cost-per-acquisition rollup across paid channels — last-click + view-through caveat, organic baseline, and a per-channel cohort lens — replaces "every channel reports a different CPA" with a single defensible view.
tags: [growth-marketing, attribution, cpa, paid-ads, multi-channel, rollup]
---
# Cross-Channel CPA Rollup

## Summary

**One-sentence:** A normalized cost-per-acquisition rollup across paid channels (Meta, Google, LinkedIn, X, organic, referral) using a documented attribution model (last-click default + view-through caveat) so weekly campaign reviews stop with "but each platform says it converted them."

**One-paragraph:** Attribution mess is the dominant pain in P-tier growth marketing: Meta claims it converted the user, Google claims the same user, LinkedIn says it nurtured, and the actual CPA the business pays is unknowable. This methodology pins five things: (1) a single attribution model (last non-direct click default, with a documented view-through window), (2) channel-level cost normalization (gross spend incl. agency fees), (3) deduplication via a unifying customer ID, (4) an organic+referral baseline so paid is not credited for organic conversions, (5) a per-channel cohort lens (cohort retention over 90 days, not single-touch CPA). Output: a weekly rollup spreadsheet + Looker/Metabase dashboard with the same numbers across the team.

## Applies If (ALL must hold)

- Business runs &gt;= 2 paid channels concurrently.
- A unifying customer ID exists (email, user ID, anonymized identifier).
- Weekly or biweekly paid-ads review is a standing ritual.
- Attribution disputes between channels have been a recurring topic.

## Skip If (ANY kills it)

- Single-channel business (only Google Ads or only one referral source) — no rollup needed.
- Pre-paid stage with no spend yet — set up the framework but populate later.
- Pure brand-building campaign with no direct-response goal — CPA is not the right metric.
- Highly regulated industry where attribution data crosses consent boundaries — consult privacy counsel first.

## Prerequisites

- Tracking layer in place (GA4, Segment, server-side tagging, or equivalent).
- Spend data export per channel (API or weekly CSV).
- Customer / conversion record store (CRM or data warehouse) with timestamps and source fields.
- A data destination for the rollup (Sheets, Looker Studio, Metabase).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/utm-discipline` | Source/medium tagging consistency assumed. |
| `pro/marketing/ppc-manager/campaign-naming-convention` | Stable campaign names assumed for grouping. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: single model, gross spend, dedup ID, organic baseline, cohort lens | ~1000 |
| `content/02-output-contract.xml` | essential | Rollup sheet shape, required columns, weekly cadence | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: double-count, missing fees, view-through abuse, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-spend-per-channel` | haiku | Mechanical from APIs / CSVs |
| `dedup-and-attribute` | sonnet | Bounded logic: pick the last non-direct touch |
| `cohort-retention-summary` | opus | Cross-channel synthesis over 90-day window |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollup-sheet.csv` | Weekly columns: channel, gross spend, attributed conversions, CPA, view-through count, 90d cohort retention |
| `templates/attribution-policy.md` | Pinned attribution model + view-through window + appeal process |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/rollup-build.py` | Read spend CSVs + conversion store; produce rollup-sheet | Weekly |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `utm-discipline`, `campaign-naming-convention`, `ppc-daily-spend-check`
- external: [Avinash Kaushik on attribution](https://www.kaushik.net/avinash/) · [GA4 attribution models](https://support.google.com/analytics)
