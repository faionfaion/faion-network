# Pain Point Research

## Summary

A systematic methodology for discovering and scoring customer pain points across public sources (Reddit, G2, App Store, Quora, Upwork). The rule: define audience + context first, mine at least 3 source tiers, capture verbatim quotes with URLs, score each pain on 5 weighted factors (Frequency 30%, Severity 25%, Reach 20%, Spend 15%, Alternatives 10%), then extract root causes via 5-Whys for the top findings.

## Why

Founders who skip structured pain-point research either miss the real problem or build for the wrong audience. Surface-level scanning of a single source produces survivorship bias and outrage artifacts. The scoring matrix converts subjective gut-feel into a comparable priority list, and 5-Whys prevents building for first-order symptoms instead of root causes.

## When To Use

- Pre-MVP: target audience defined but no validated problem yet.
- Choosing between 3-5 candidate ideas — score the underlying pains to break ties.
- Exploring an unfamiliar niche where domain intuition is weak.
- Repurposing existing research (G2 reviews, Reddit threads) into a structured opportunity backlog.

## When NOT To Use

- You already have paying users — switch to user interviews and cancellation post-mortems; stranger pain points add noise.
- Highly regulated domains (healthcare, finance) where complaints are NDA'd and public signal is misleading.
- B2B enterprise where buyers don't post complaints publicly — use expert calls and analyst reports instead.
- Quantitative effect sizes are required — this methodology yields qualitative signal only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-discovery-framework.xml` | Source tiers (Tier 1-4), search patterns per source, scope definition template, and the 5-Whys root-cause method. |
| `content/02-scoring-and-categorization.xml` | Eight pain categories, the 5-factor scoring matrix with weights, priority thresholds, and antipatterns in scoring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pain-point-log.md` | Research log template: scope, PP-NNN entries with scores, summary by category, top-5 list. |
| `templates/reddit-mining.md` | Reddit-specific extraction template with posts analyzed, pain points found, notable quotes. |
| `templates/batch-scorer.py` | Python script: reads JSON list of pain points, computes weighted score, outputs CSV. |
