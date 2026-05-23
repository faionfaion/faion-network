---
slug: google-display-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Display campaign spec: audience layering (in-market + affinity + custom + remarketing), placement controls (exclude apps, low-quality sites), creative set (responsive + native + image).
content_id: "77dc5189848f7593"
complexity: medium
produces: spec
est_tokens: 4400
tags: [google-display, display-network, remarketing, awareness, placements]
---
# Google Display Network Strategy

## Summary

**One-sentence:** Produces a Display campaign spec: audience layering (in-market + affinity + custom + remarketing), placement controls (exclude apps, low-quality sites), creative set (responsive + native + image).

**One-paragraph:** Display Network is awareness/upper-funnel; conversion expectations must be calibrated. Methodology forces audience layering (in-market + affinity + custom + remarketing), heavy placement exclusions (mobile apps unless intentional; low-quality sites via topic+placement exclusion lists), and a responsive + native + image creative set with frequency caps.

**Ефективно для:**

- Awareness / upper-funnel — Display Network для top-of-funnel reach.
- Audience layering: in-market + affinity + custom intent + remarketing.
- Heavy placement exclusions (mobile apps, low-quality sites).
- Frequency caps + custom audiences для CPA <$50 ceiling.

## Applies If (ALL must hold)

- Awareness / upper-funnel campaign that paired Search cannot fill.
- Remarketing layer over an existing Search account.
- Custom-intent audience experiments at low CPC.
- Brand-safety project demanding placement audit.

## Skip If (ANY kills it)

- Direct-response campaigns expecting Search-level CPA — wrong channel.
- <$1k/mo budget — Display needs reach floor.
- No remarketing list ≥1000 — half the leverage gone.
- No creative inventory beyond text — responsive ads alone perform poorly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Account foundation | report | google-ads-basics |
| Audience inventory | lists | ads-google-keywords + remarketing |
| Creative inventory (banner + native + responsive) | library | creative |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/google-ads-basics` | Foundation must be in place. |
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion events required to judge channel. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-display-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audience-layering` | sonnet | Per-stage audience tier selection. |
| `exclusion-list` | haiku | Apply the standard exclusion list. |
| `creative-coverage` | haiku | Coverage across 3 formats. |

## Templates

| File | Purpose |
|------|---------|
| `templates/display-spec.md` | Display campaign spec Markdown skeleton. |
| `templates/placement-exclusions.csv` | Standard placement exclusion list seed. |
| `templates/display-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-display-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[google-ads-basics]]
- [[google-ads-optimization]]
- [[ads-retargeting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
