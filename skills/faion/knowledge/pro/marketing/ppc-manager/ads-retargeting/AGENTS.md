---
slug: ads-retargeting
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a funnel-stage retargeting plan: segment by intent (visitors → blog → product → pricing → cart), per-segment message + frequency caps + exclusion rules; 20-30% of total ad spend.
content_id: "074e1b4cf8a47527"
complexity: medium
produces: spec
est_tokens: 4400
tags: [retargeting, remarketing, funnel, audiences, conversion-optimization]
---
# Retargeting / Remarketing

## Summary

**One-sentence:** Produces a funnel-stage retargeting plan: segment by intent (visitors → blog → product → pricing → cart), per-segment message + frequency caps + exclusion rules; 20-30% of total ad spend.

**One-paragraph:** Full-funnel retargeting. Segment past visitors by intent depth (all visitors → blog readers → product viewers → pricing viewers → cart abandoners), tailor message per stage, apply frequency caps to prevent fatigue, exclude recent converters from acquisition campaigns. Retargeting should be 20-30% of total spend and typically delivers 40-70% lower CPA vs cold prospecting.

**Ефективно для:**

- Pixel installed, ≥1000 site visitors / month — стандартний retargeting source.
- Post-prospecting funnel: recover non-converters within 7-30 днів.
- Sequential ad sequences: reminder → benefits → social proof → urgency.
- Upsell / cross-sell на past purchasers з exclusion на recent buyers.

## Applies If (ALL must hold)

- Pixel installed + website segments ≥1000 each.
- Post-prospecting funnel where non-converters need recovery.
- Sequential ad sequences (reminder → benefits → social proof → urgency).
- Upsell / cross-sell to past purchasers with exclusion of recent buyers.

## Skip If (ANY kills it)

- Pixel not installed / not verified — audiences won't populate.
- Any retarget audience under 1000 — delivery throttled.
- Frequency already >5 with CTR declining — pause and refresh creative first.
- Brand-awareness only campaigns with no defined conversion event.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pixel + CAPI live | dashboard | ads-conversion-tracking |
| Pixel event taxonomy | schema doc | ads-conversion-tracking |
| Creative inventory per funnel stage | CSV | ads-meta-creative |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Pixel events seed every retargeting segment. |
| `pro/marketing/ppc-manager/ads-meta-creative` | Per-stage creative supplies the message variants. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-retargeting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intent-ladder` | sonnet | Map pixel events → intent depth + stage. |
| `frequency-matrix` | haiku | Mechanical per-tier cap assignment. |
| `exclusion-policy` | haiku | Pixel.Purchase + CRM → exclusion list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retargeting-plan.md` | Retargeting plan Markdown skeleton with the 5-tier ladder. |
| `templates/frequency-matrix.csv` | Per-stage frequency cap matrix. |
| `templates/retargeting-plan.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-retargeting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-targeting]]
- [[ads-conversion-tracking]]
- [[ads-attribution-models]]
- [[meta-audience-targeting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
