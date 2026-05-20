---
slug: build-in-public-content-engine
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a831757418725d9e"
summary: End-to-end build-in-public content engine for solo founders — cadence, formats, hook patterns, repurposing chain, and metric loop — packaged as a single playable system.
tags: [build-in-public, indie-hacker, content-engine, twitter-x, audience-growth]
---
# Build-in-Public Content Engine

## Summary

**One-sentence:** A single, end-to-end content engine that turns a solo founder's weekly product work into a sustainable build-in-public cadence with formats, hooks, repurposing, and a measurable feedback loop — designed for the indie hacker who "dislikes marketing."

**One-paragraph:** Build-in-public is the dominant indie-hacker growth motion, but it is currently implicit across `twitter-x-growth`, `content-marketing`, and `lean-marketing`. The result is solos cherry-pick tactics and quit at week 6. This methodology consolidates the motion into one playable system: weekly inputs (what you shipped, what broke, what you learned, one number) -> standard formats (build-log post, learning post, screenshot/demo, number-of-the-week, ask post) -> hook patterns -> repurposing chain (X -> LinkedIn -> Substack/blog -> newsletter) -> metric loop (compound followers / list / inbound). Output: a 6-week cadence with measurable subscriber and reply growth, run in <= 4 hours/week.

## Applies If (ALL must hold)

- Founder is actively building a product (shipping or close to shipping weekly).
- Founder is willing to share work publicly (numbers, mistakes, screenshots).
- A primary channel is selected (default: X) and an account exists with a basic bio.
- Founder can commit at least 3 short posts + 1 longer post per week.

## Skip If (ANY kills it)

- Product is in stealth or under enterprise NDA — no public sharing possible.
- Founder has zero tolerance for public commentary — engine fails on internal resistance.
- Target ICP is not on social media (e.g., construction trades, hospital procurement) — switch to outbound + community methodology.
- Founder has &lt; 1 hour/week available — engine requires minimum 3-4 hrs/week to sustain compound effect.

## Prerequisites

- A weekly product-work log (commits, decisions, screenshots) — can be a Notion page or a markdown journal.
- One primary social account active (default: X with handle, bio, banner).
- A simple email-capture page (Substack, ConvertKit, or static page with mailer) — repurposing chain ends in a list.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/content-marketing` | General content fundamentals (CTA, hook) assumed; not re-taught here. |
| `solo/marketing/seo-manager/seo-essentials` | Long-form repurposing benefits from minimal SEO; load if writing public posts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: weekly input ritual, format menu, hook discipline, repurposing chain, metric loop | ~1000 |
| `content/02-output-contract.xml` | essential | Weekly batch shape, posting cadence, KPI floor at month 1/3/6 | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: vanity-only metrics, generic LLM posts, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `weekly-log-to-post-drafts` | sonnet | Bounded transformation from journal entries to post candidates |
| `hook-line-variation` | haiku | Mechanical: produce 5 hook variants per draft |
| `monthly-engine-review` | opus | Synthesis: what's working, what to drop, where to amplify |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-input-log.md` | What I shipped / what broke / what I learned / one number |
| `templates/post-formats.md` | The 5 standard formats with example posts and hook patterns |
| `templates/repurposing-checklist.md` | X -> LinkedIn -> blog -> newsletter conversion rules |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/engine-metrics.py` | Aggregate weekly follower / list / inbound numbers; produce trend chart | Weekly |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodology: `twitter-x-growth`, `content-marketing`, `newsletter-engine`
- external: [Pieter Levels — Build in Public](https://twitter.com/levelsio) · [Arvid Kahl — The Embedded Entrepreneur](https://embeddedentrepreneur.com/)
