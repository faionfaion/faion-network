---
slug: objection-bank
tier: solo
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "05a6be50857e6c76"
summary: A living objection bank discipline that captures every recurring buyer objection from outreach, landing-page bounces, and sales calls into a single, ranked, regularly-updated artifact tied back to landing copy and FAQ.
tags: [sales, objection-handling, landing-pages, outreach, faq, indie-hacker]
---

# Objection Bank for Solo Outreach and Launches

## Summary

**One-sentence:** Maintain a single ranked file (`objection-bank.yaml`) of every objection that surfaces in cold DMs, sales calls, Product Hunt launches, and landing-page bounces, with a counter-statement and a tie-back to the page/section where the objection should be answered.

**One-paragraph:** Every cold-outreach loop, every Product Hunt launch, every demo call surfaces the same 8-12 objections. Solo founders either re-discover them every launch ("nobody mentioned the GDPR concern last time") or write them into an internal Notion page that no living person updates. The objection-bank pattern formalises the artifact: every objection-touching encounter ends with an `objections-mentioned` field in the encounter log, a weekly script merges them into the ranked bank with frequency and tie-back-to-copy, and landing-page reviews start with "for the top-5 objections, is the answer above the fold?". Mechanism: capture → rank by frequency × revenue-impact → tie each to the FAQ entry or landing-page section that should resolve it → review monthly. Primary output: `objection-bank.yaml` checked into the marketing repo, plus monthly diff posted to the founder's marketing channel.

## Applies If (ALL must hold)

- founder runs at least one outbound channel: cold DMs, Reddit, Product Hunt launches, Twitter/X build-in-public, newsletter
- founder takes at least 2 sales / demo calls per month OR has at least 500 landing-page visits per month
- product has been live (or in private beta with paying customers) for ≥ 30 days
- founder maintains landing copy themselves (no separate copywriter who would block edits)

## Skip If (ANY kills it)

- founder is pre-product with no outreach yet — capture conversations informally, formalise the bank after the first 20 conversations
- enterprise sales with a dedicated SDR team — use the SDR's CRM objection-field instead, do not duplicate
- product has zero objections (genuinely commodity utility, e.g. status-page checker) — objections are not the limiter; pricing / awareness is
- founder cannot edit landing copy on their own (gated by a marketing team) — the tie-back loop breaks; capture without ownership becomes shelfware

## Prerequisites

- a single Markdown / YAML file location agreed (typically `marketing/objection-bank.yaml` in the same repo as the landing page)
- a tag taxonomy (price, feature-gap, trust, security, switching-cost, integration) drafted before the first entry
- a calendar habit: 15 minutes per Friday to merge the week's encounters into the bank

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/gtm-strategist/growth-cold-outreach` | Cold-outreach loop is one of the bank's main input streams |
| `solo/marketing/seo-manager/zero-click-search-adaptation` | Landing-page section structure where objection answers live |
| `pro/marketing/conversion-optimizer/funnel-tactics-basics` | Tie-back loop assumes funnel-stage awareness for placement decisions |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: capture-at-source, rank-by-frequency-and-revenue, tie-back-to-copy, monthly-diff, one-objection-one-counter | ~900 |
| `content/02-output-contract.xml` | essential | objection-bank.yaml schema with required fields, forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: synthetic objections, stale entries, tag bloat, untied entries, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_objection_from_conversation_log` | sonnet | Bounded extraction with judgment on tagging |
| `cluster_near_duplicate_objections` | sonnet | Per-pair similarity judgment |
| `propose_landing_page_tie_back` | sonnet | Maps objection to landing section; bounded |
| `monthly_diff_synthesis` | sonnet | Cross-objection trend analysis for the founder summary |

## Templates

| File | Purpose |
|------|---------|
| `templates/objection-bank.yaml` | YAML schema with all fields wired up |
| `templates/encounter-log-snippet.md` | Footer snippet to append to every demo call note, every PH-launch retro, every cold-outreach log |
| `templates/monthly-diff-post.md` | Skeleton for the monthly "what changed" post |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/merge-encounters.py` | Reads encounter logs from the past week, surfaces new objections for human review before merging into the bank | Friday 15-min weekly habit |
| `scripts/landing-tie-back-audit.py` | Walks the top-5 ranked objections, checks whether each has an answer in the landing copy above the fold | Monthly |

## Related

- parent skill: `solo/marketing/gtm-strategist/SKILL.md`
- peer methodologies: `solo/marketing/gtm-strategist/growth-cold-outreach`, `solo/marketing/content-marketer/growth-copywriting-fundamentals`
- external: [Voss, Never Split the Difference (Random House, 2016) Chapter 4 on labels and accusations audit] · [Bencivenga, "Bullets" methodology for objection-led copy] · [April Dunford, Obviously Awesome (chapter on context shifting)]
