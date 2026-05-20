---
slug: tweet-thread-launch-template
tier: solo
group: marketing
domain: smm-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4afdde69ef09d9fe"
summary: A 7-tweet launch-thread structure (hook → demo gif → problem → solve → price → CTA → social proof) optimised for the indie-hacker Twitter/X audience and Product Hunt launch day.
tags: [twitter-x, launch, indie-hacker, copywriting, product-hunt]
---

# Tweet Thread Launch Template

## Summary

**One-sentence:** A 7-tweet launch-thread structure (hook → demo gif → problem → solve → price → CTA → social proof) optimised for the indie-hacker Twitter/X audience and Product Hunt launch day.

**One-paragraph:** Indies launch on Twitter/X, not press releases. The thread is the launch instrument: it carries the hook, the demo, the price, and the CTA in 7 tweets. Generic copywriting-fundamentals + twitter-x-growth don't specify the launch-thread shape. This methodology pins the 7-tweet structure with character limits per tweet, mandatory media slots (demo gif tweet 2, social proof screenshot tweet 7), CTA discipline (one link, end of tweet 6), and the launch-day timing pattern. Output: a structured `LaunchThread` JSON ready to paste into Twitter, Typefully, or Hypefury.

## Applies If (ALL must hold)

- product / feature launching publicly (paid SaaS, freemium, free tool with attention goal)
- operator has ≥ 500 followers on Twitter/X (otherwise reach is too thin)
- demo gif / video exists OR can be produced in &lt; 4h
- launch day is set (not "soon") and within next 14 days

## Skip If (ANY kills it)

- product is enterprise / SOC-2 / regulated — Twitter launch is wrong channel
- operator has &lt; 100 followers — build audience first; threads to empty rooms underperform
- launch is a major rewrite of an existing product without a new value prop — relaunches need different structure
- operator hates Twitter — authenticity matters; ghostwritten thread underperforms

## Prerequisites

- working demo / screenshot / 6-15s gif (mandatory)
- short positioning statement (from `solo-niche-narrative-framework`)
- price + plan structure
- launch day + landing-page URL
- 1-2 early-user quotes for tweet 7 (social proof)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Provides the audience-building context this launch lands on |
| `pro/marketing/gtm-strategist/solo-niche-narrative-framework` | Feeds the positioning statement used in tweet 3-4 |
| `pro/marketing/growth-marketer/product-hunt-launch` | Sister methodology for the PH-specific launch tasks |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 7-tweet shape, character limits, media slots, single CTA, social-proof verbatim | ~900 |
| `content/02-output-contract.xml` | essential | `LaunchThread` JSON schema with per-tweet schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: hook-buried, multi-CTA, fake-proof, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hook_generation` | opus | Single-shot judgment on the most important sentence |
| `body_tweet_draft` | sonnet | Per-tweet drafting with structure |
| `cta_line` | sonnet | Bounded copy |
| `social_proof_extraction` | sonnet | Verbatim quote shaping |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-thread.json` | Output schema |
| `templates/thread-shell.md` | Manual draft template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/preview-thread.py` | Render thread for visual check | Before scheduling |
| `scripts/schedule-typefully.sh` | Push to Typefully API | T-1h before launch |

## Related

- parent skill: `solo/marketing/smm-manager/`
- peer methodologies: `growth-twitter-x-growth`, `product-hunt-launch`
- external: [Marc Lou — How to launch on Twitter](https://shipfa.st/) · [Tony Dinh — Indie launches](https://tonydinh.com/) · [Typefully — Thread anatomy](https://typefully.com/blog/twitter-thread) · [Pieter Levels — Launch how-to](https://levels.io/)
