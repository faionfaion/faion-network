---
slug: google-shopping-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Shopping campaign spec: Merchant Center feed health, product-group structure, priority-tier campaigns (high/medium/low) for inventory segmentation, negative-keyword sweep on Shopping.
content_id: "c50ed176960a4dc8"
complexity: medium
produces: spec
est_tokens: 4400
tags: [google-shopping, merchant-center, product-feed, roas, negative-keywords]
---
# Google Shopping Ads

## Summary

**One-sentence:** Produces a Shopping campaign spec: Merchant Center feed health, product-group structure, priority-tier campaigns (high/medium/low) for inventory segmentation, negative-keyword sweep on Shopping.

**One-paragraph:** Shopping is the dominant ecom channel on Google. Methodology pins Merchant Center feed health as the foundation (titles, GTIN, images, attributes), splits inventory into priority-tier campaigns (high-margin / mid / clearance) for targeted ROAS, sets product groups by margin or category, and applies negative keywords (Shopping does not use keywords for bidding but DOES honor negatives to exclude irrelevant queries).

**Ефективно для:**

- Ecom з активним product feed у Merchant Center.
- Multi-tier inventory: high-margin / mid / clearance.
- Product groups з ≥30 conversions / tier per month.
- Negative-keyword sweep на Shopping queries.

## Applies If (ALL must hold)

- Ecom with active product feed in Merchant Center.
- Multi-tier inventory pricing (high-margin / mid / clearance).
- Conversion volume ≥30 per tier per month.
- Brand + non-brand split desired.

## Skip If (ANY kills it)

- Lead-gen / B2B SaaS — Shopping does not apply.
- Feed health <80% (missing titles, GTIN, images) — fix feed first.
- Single-SKU or service business — overhead exceeds payoff.
- Newly launched store <60 days — no signal yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Merchant Center setup + product feed | feed | merchant |
| Feed health audit (≥80% complete) | report | merchant |
| Margin / category taxonomy | CSV | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/google-ads-basics` | Foundation must be in place. |
| `pro/marketing/ppc-manager/google-ads-optimization` | Optimization cycle applies on top. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-shopping-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feed-audit` | sonnet | Title / GTIN / image quality judgement. |
| `tier-split` | sonnet | Margin taxonomy + ROAS target derivation. |
| `negative-list-build` | haiku | Apply standard ecom negative list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/shopping-spec.md` | Shopping campaign spec Markdown skeleton. |
| `templates/feed-health-checklist.md` | Feed health audit checklist. |
| `templates/shopping-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-shopping-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[google-ads-basics]]
- [[google-pmax]]
- [[google-ads-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
