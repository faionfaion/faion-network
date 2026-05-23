---
slug: google-search-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Search campaign spec: keyword + ad-group structure, match-type mix (broad + phrase + exact), 3-RSA-per-group rule, quality-score gates, sitelink + callout floor.
content_id: "a6a5463c0f35bfbf"
complexity: medium
produces: spec
est_tokens: 4400
tags: [google-search, rsa, match-types, quality-score, extensions]
---
# Google Search Ads

## Summary

**One-sentence:** Produces a Search campaign spec: keyword + ad-group structure, match-type mix (broad + phrase + exact), 3-RSA-per-group rule, quality-score gates, sitelink + callout floor.

**One-paragraph:** Google Search is the high-intent workhorse of paid. Methodology pins the modern structure: 1 ad group per intent, 3 RSAs (Responsive Search Ads) per ad group with diversified headlines, match-type mix (broad with smart bidding for discovery; phrase/exact for guard), QS≥7 gate, and mandatory sitelinks + callouts. Goal: max QS × intent fit, not cheapest CPC.

**Ефективно для:**

- High-intent acquisition: bottom of funnel.
- Intent → ad group (10-20 keywords, 1 theme).
- RSAs × 3 на group з diversified headlines.
- QS≥7 gate + sitelinks/callouts mandatory.

## Applies If (ALL must hold)

- High-intent acquisition campaign (bottom-of-funnel).
- Keyword-driven demand capture with measurable conversion.
- Multi-product accounts requiring per-product ad groups.
- Brand-protection campaigns (brand search defense).

## Skip If (ANY kills it)

- Awareness-only — Display/PMax fits better.
- No keyword research available — different methodology (ads-google-keywords).
- <$500/mo Search budget — overhead exceeds payoff.
- Trademark-disputed brand — legal must clear first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Keyword research | CSV | ads-google-keywords |
| Account foundation | report | google-ads-basics |
| RSA headline/description inventory | library | creative |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/google-ads-basics` | Foundation. |
| `pro/marketing/ppc-manager/ads-google-keywords` | Keyword research input. |
| `pro/marketing/ppc-manager/ads-google-creative` | RSA copy input. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-search-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intent-grouping` | sonnet | Keyword → intent assignment with judgement. |
| `rsa-drafts` | sonnet | Headline + description copy. |
| `extensions-fill` | haiku | Apply standard floor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/search-spec.md` | Search campaign spec Markdown skeleton. |
| `templates/rsa-template.md` | RSA headline + description template (3 variants). |
| `templates/search-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-search-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[google-ads-basics]]
- [[ads-google-keywords]]
- [[ads-google-creative]]
- [[google-ads-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
