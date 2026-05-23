---
slug: instagram-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an Instagram campaign spec: Reels + Stories + Feed placement mix, UGC + creator content gate, 9:16-first creative, Shopping tags for ecom, IG-specific frequency caps.
content_id: "8e23223d728ee837"
complexity: medium
produces: spec
est_tokens: 4400
tags: [instagram-ads, reels, stories, ugc, shopping-tags]
---
# Instagram Ads Playbook

## Summary

**One-sentence:** Produces an Instagram campaign spec: Reels + Stories + Feed placement mix, UGC + creator content gate, 9:16-first creative, Shopping tags for ecom, IG-specific frequency caps.

**One-paragraph:** Instagram is the visual-first Meta surface. Methodology forces 9:16 / Reels-first creative, mandates UGC or creator content for cold acquisition, gates placement on creative format (Reels must be vertical video; Stories must be 9:16; Feed accepts 1:1 / 4:5), wires Shopping tags for ecom, and applies IG-specific frequency caps (lower than FB).

**Ефективно для:**

- B2C / lifestyle / DTC з main audience на IG.
- Reels-first 9:16 video budget доступний.
- UGC або creator content для cold prospecting.
- Ecom з Instagram Shopping tags + product feed.

## Applies If (ALL must hold)

- B2C / lifestyle / DTC product with main audience on IG.
- Reels-first creative strategy (9:16 video budget).
- Ecom with Instagram Shopping tags + product feed.
- Creator / UGC partnership for cold acquisition.

## Skip If (ANY kills it)

- B2B with Director+ ICP — LinkedIn / Search beat IG.
- Audience primarily on Facebook feed — facebook-ads methodology.
- No 9:16 video budget — Reels won't perform.
- No UGC / creator inventory for cold — only retargeting will work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Instagram Business + linked FB Page | dashboard | platform owner |
| Pixel + CAPI + Shopping tags (ecom) | config | ads-conversion-tracking |
| Creator / UGC pipeline | library | creative |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-meta-campaign-setup` | Generic Meta rules apply on top. |
| `pro/marketing/ppc-manager/ads-meta-creative` | Per-format creative brief. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for instagram-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `placement-allocation` | haiku | Apply Reels-first rule. |
| `creative-strategy` | sonnet | UGC / creator vs brand-polished mapping. |
| `shopping-tag-setup` | haiku | Feed-linkage check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/instagram-spec.md` | Instagram campaign spec Markdown skeleton. |
| `templates/ugc-brief.md` | UGC / creator content brief Markdown skeleton. |
| `templates/instagram-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-instagram-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-campaign-setup]]
- [[ads-meta-creative]]
- [[ads-meta-targeting]]
- [[facebook-ads]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
