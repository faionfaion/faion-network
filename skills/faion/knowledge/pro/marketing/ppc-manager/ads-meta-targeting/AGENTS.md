---
slug: ads-meta-targeting
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a 3-tier Meta audience spec: Core (interest/demo/behavior), Custom (pixel + email + engagement), Lookalike (1% / 2-3% / 5-10%); exclusion audiences + Advantage+ gate.
content_id: "60f67302bd15970f"
complexity: medium
produces: spec
est_tokens: 4400
tags: [meta-ads, targeting, audiences, lookalike, custom-audiences]
---
# Meta Audience Targeting (3-Tier)

## Summary

**One-sentence:** Produces a 3-tier Meta audience spec: Core (interest/demo/behavior), Custom (pixel + email + engagement), Lookalike (1% / 2-3% / 5-10%); exclusion audiences + Advantage+ gate.

**One-paragraph:** Three-tier audience strategy for Meta. Core for cold traffic, Custom for warm, Lookalike for scaling. Exclusions (purchasers + subscribers) MUST be set before any campaign launches. Advantage+ is allowed only for broad-appeal products with budget ≥ $100/day; below that, manual targeting wins. Output is an audience spec covering each tier with size guards + match-quality checks.

**Ефективно для:**

- Setup аудиторій перед launch Meta-кампанії.
- Scaling Core → Lookalike коли є ≥1000 quality source.
- Retargeting на pixel behavior (cart, pricing, checkout).
- A/B Core vs LAL vs retarget — який tier дає nижчий CPA.

## Applies If (ALL must hold)

- Setting up audiences before launching any Meta campaign.
- Scaling: expanding Core into Lookalike on the back of a quality source ≥1000.
- Retargeting by pixel behavior (pricing page, cart, checkout).
- A/B comparing audience-tier CPA (Core vs LAL vs retargeting).

## Skip If (ANY kills it)

- Core/Interest audience under 500K — delivery throttled, CPM spike.
- Lookalike source under 1000 people — match quality poor; grow source first.
- Advantage+ on niche product or small budget — Meta AI needs scale.
- Pixel not installed or verified — Custom/LAL won't populate correctly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pixel + CAPI live | dashboard verification | ads-conversion-tracking |
| ICP definition | JSON | GTM |
| CRM purchaser / subscriber lists | CSV / hashed emails | RevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Pixel events seed Custom + Lookalike audiences. |
| `pro/marketing/ppc-manager/ads-meta-campaign-setup` | Audience plan feeds the ad-set layer in campaign setup. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-meta-targeting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size-core` | haiku | Mechanical: interest filter set → size estimate from Meta. |
| `pick-lal-pct` | sonnet | Source size + scale goal → 1% / 2-3% / 5-10%. |
| `exclusions-derivation` | haiku | CRM lists + pixel events to exclusions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-spec.md` | Three-tier audience spec Markdown skeleton. |
| `templates/exclusions-checklist.md` | Exclusion audiences checklist before launch. |
| `templates/audience-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-meta-targeting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-campaign-setup]]
- [[ads-meta-creative]]
- [[ads-retargeting]]
- [[meta-audience-targeting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
