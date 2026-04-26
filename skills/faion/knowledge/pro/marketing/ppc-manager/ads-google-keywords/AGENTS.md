# Google Ads Keyword Strategy

## Summary

Intent-first keyword research and organization for Google Search campaigns. Research seed keywords, classify by search intent (transactional/commercial/informational/navigational), assign match types (phrase/exact/broad), cluster into themed ad groups of 10-20 keywords, and maintain a shared negative list. Harvest Search Terms weekly to promote winners to exact match and add irrelevant queries as negatives.

## Why

Targeting the wrong keywords wastes budget on irrelevant clicks. Broad-only campaigns bleed spend; no negatives compounds the problem. Organizing by intent ensures ad copy matches what the searcher expects, improving Quality Score (expected CTR + ad relevance + landing page experience) and lowering CPA.

## When To Use

- Building a new search campaign from scratch (seed → expand → cluster → match type → negatives).
- Weekly Search Terms Report mining: extract negatives, promote winners to exact, find new themes.
- Migrating a broad-only account to phrase + exact + tight-negatives structure.
- Reorganizing an ad group with 100+ keywords across mixed intents.

## When NOT To Use

- Performance Max — pmax doesn't expose keywords; use audience signals + asset groups instead.
- Smart campaigns — Google picks keywords; your input is themes, not keyword lists.
- Display/YouTube — keywords are hint-only; topics + audiences dominate.
- Brand-only campaigns with a well-converged list — agent loops add noise.

## Content

| File | What's inside |
|------|---------------|
| `content/01-keyword-strategy.xml` | Intent taxonomy, match-type rules, ad-group structure, negative-list policy. |
| `content/02-workflow.xml` | Build workflow (one-shot per group) and weekly harvest loop with agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/keyword-plan.md` | Keyword research spreadsheet columns + ad-group plan structure. |
| `templates/negative-keyword-list.md` | Shared negative list with Unqualified/Wrong-Intent/Wrong-Audience sections. |
| `templates/harvest-search-terms.py` | Google Ads API script to pull Search Terms and classify them. |
