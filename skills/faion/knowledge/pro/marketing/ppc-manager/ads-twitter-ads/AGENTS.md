---
slug: ads-twitter-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an X/Twitter campaign spec: objective + audience (follower-LAL, keyword, conversation, interest), promoted-tweet format, bid strategy, with brand-safety + viewability guards.
content_id: "31822c789464c9d6"
complexity: medium
produces: spec
est_tokens: 4400
tags: [x-ads, twitter-ads, social-ads, promoted-tweet, brand-safety]
---
# X / Twitter Ads Strategy

## Summary

**One-sentence:** Produces an X/Twitter campaign spec: objective + audience (follower-LAL, keyword, conversation, interest), promoted-tweet format, bid strategy, with brand-safety + viewability guards.

**One-paragraph:** X/Twitter is a niche acquisition channel after 2023 platform changes. Methodology gates spend on audience-fit (B2B + tech + crypto + media verticals), forces brand-safety controls, and pins the promoted-tweet format with a max-2-emoji policy. Output is a campaign spec covering objective, audience (follower-LAL, keyword, conversation, interest), bid strategy, and reporting cadence.

**Ефективно для:**

- B2B / tech / crypto / media — де X audience fit платить.
- Follower-Lookalike або keyword targeting на active threads.
- Brand-safety controls + viewability >50% guard.
- Promoted-tweet з max-2-emoji policy.

## Applies If (ALL must hold)

- B2B / tech / crypto / media product where X audience fits.
- Follower-Lookalike or keyword targeting on active threads.
- Brand-safety-aware buying with explicit content-category exclusions.
- Engagement / clicks / followers objective with measurable funnel.

## Skip If (ANY kills it)

- Mass-consumer / non-tech vertical — X audience does not match.
- Daily budget < $50 — auction floor wastes signal.
- No brand-safety category exclusion list — content-adjacency risk.
- Performance-only KPI (CPA) on cold X — channel rarely beats Meta on direct response.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| X Ads account access | OAuth | platform owner |
| Brand-safety category exclusion list | JSON | brand |
| Audience hypothesis | doc | GTM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Pixel events for X conversion API. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-twitter-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audience-mode` | sonnet | Choose LAL vs keyword vs conversation per ICP. |
| `brand-safety-list` | haiku | Apply standard exclusion list. |
| `tweet-copy` | sonnet | Hook + CTA + ≤2 emoji. |

## Templates

| File | Purpose |
|------|---------|
| `templates/campaign-spec.md` | X campaign spec Markdown skeleton. |
| `templates/brand-safety-exclusions.json` | Standard brand-safety category exclusion list. |
| `templates/campaign-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-twitter-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-targeting]]
- [[ads-linkedin-ads]]
- [[ads-conversion-tracking]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
