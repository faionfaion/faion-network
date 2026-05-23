---
slug: google-pmax
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a PMax spec: asset-group structure (≥3 groups), audience signals + listing groups for ecom, exclusion lists, conversion-value priority, brand-bidding guardrails.
content_id: "b0edf1f332cb581f"
complexity: medium
produces: spec
est_tokens: 4400
tags: [google-pmax, performance-max, shopping, asset-groups, audience-signals]
---
# Google Performance Max

## Summary

**One-sentence:** Produces a PMax spec: asset-group structure (≥3 groups), audience signals + listing groups for ecom, exclusion lists, conversion-value priority, brand-bidding guardrails.

**One-paragraph:** Performance Max is Google's blended-channel auto-bid product. It punishes accounts without a strong conversion signal and hides spend in opaque asset-group buckets. Methodology gates PMax on ≥30 conv/mo, forces ≥3 asset groups by theme, pins audience signals for cold start, applies brand-bidding negatives, and demands value-priority on conversion events.

**Ефективно для:**

- Account з ≥30 conversions/month + chronic spend ≥$5k/mo.
- Multi-channel scale: search + shopping + display + YouTube + Gmail в one campaign.
- Ecom з product feed для Shopping-blended PMax.
- Audience signals для cold-start acceleration.

## Applies If (ALL must hold)

- Account with ≥30 conv/mo and a Search/Shopping baseline.
- Ecom with product feed (Shopping integration).
- Lead-gen with strong offline conversion API.
- Scaling beyond Search inventory (YouTube + Display + Gmail blended).

## Skip If (ANY kills it)

- <30 conv/mo — PMax cannot learn; budget lost in opaque buckets.
- Brand-protection-only accounts — PMax cannibalizes brand Search.
- No conversion-value signal (offline or online) — auto-bid wanders.
- Audit cycle pending — opaque reporting will fight the audit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Conversion API + value priority | config | ads-conversion-tracking |
| Product feed / merchant center (ecom) | feed | merchant |
| Brand-bidding negatives list | CSV | brand |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/google-ads-basics` | Foundation must be in place; PMax layers on top. |
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Value priority + offline conversion API drive PMax. |
| `pro/marketing/ppc-manager/google-shopping-ads` | Shopping methodology supplies the product feed quality. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-pmax | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `asset-group-split` | sonnet | Theme partitioning needs judgement. |
| `audience-signals` | sonnet | Per-group signal stack. |
| `brand-negatives` | haiku | Apply brand list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pmax-spec.md` | PMax spec Markdown skeleton with asset groups + signals + negatives. |
| `templates/brand-negatives.csv` | Brand negatives seed CSV. |
| `templates/pmax-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-pmax.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[google-ads-basics]]
- [[google-ads-optimization]]
- [[google-shopping-ads]]
- [[ads-conversion-tracking]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
