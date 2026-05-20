---
slug: messaging-house-template
tier: solo
group: marketing
domain: content-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A concrete fillable messaging house template tying one-line value → 3 pillars → proof points → per-channel variants.
content_id: "5e69dfa10d71ee06"
tags: [messaging,positioning,launch,pillars,proof-points,channel-variants]
---
# Messaging House Template

## Summary

**One-sentence:** A concrete fillable messaging house template tying one-line value → 3 pillars → proof points → per-channel variants.

**One-paragraph:** Brand-positioning methodology exists, but teams lack the single artifact that connects positioning to per-channel copy — so launch copy diverges, channels contradict, and the buyer hears three different value props from three places. This methodology defines the messaging house: one root-line value statement at the top, exactly 3 pillars supporting it, each pillar carries 2-4 proof points (data, customer quote, demo asset), and each pillar produces per-channel variants (X tweet, LinkedIn post, email subject, ad copy, landing-page hero). Mechanism: closed-structure house, evidence requirement per proof point, channel-variant compactness rules. Primary output: a single one-page house artifact owned by content lead and referenced by every launch asset.

## Applies If (ALL must hold)

- product has ≥ 1 confirmed positioning statement OR is preparing for major launch
- launch involves ≥ 3 channels OR launch sequence ≥ 2 weeks long
- ≥ 2 contributors are writing copy across channels
- positioning research exists (interviews, competitive analysis, JTBD)
- content lead exists with editorial authority

## Skip If (ANY kills it)

- pre-positioning stage — finish JTBD / value-proposition design first
- single-tweet launch with no follow-up content — overhead beats payoff
- regulated product where claims require legal-approval flow per channel
- maintenance-mode product with no new positioning
- team already operates a kept-updated messaging house (avoid duplication)

## Prerequisites (must be true before starting)

- root value-statement candidate (one sentence)
- list of ≥ 3 candidate pillars (areas of value)
- ≥ 6 evidence items (customer quotes, data, demos) available for proof points
- target channels named (X, LinkedIn, email, ads, landing)
- agreed-upon tone (Brand Voice doc OR examples)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/value-proposition-design` | Source of root value statement |
| `solo/research/researcher/jtbd` | Pillar candidates may be JTBD-derived |
| `pro/marketing/growth-marketer/launch-day-warroom-template` | Consumer of the messaging house at launch time |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: one root value, exactly 3 pillars, ≥ 2 proof points per pillar, channel-variant rule, content-lead ownership | ~1000 |
| `content/02-output-contract.xml` | essential | House schema, channel-variant fields, evidence requirements | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (pillar inflation, weak proof points, off-tone variants, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `value_statement_critique` | sonnet | Sharpen root sentence, remove waffle |
| `pillar_proof_synth` | sonnet | Match proof points to pillars |
| `channel_variant_writer` | sonnet | Generate per-channel copy preserving pillar |
| `tone_consistency_scanner` | haiku | Scan variants for tone drift vs Brand Voice doc |

## Templates

| File | Purpose |
|------|---------|
| `templates/messaging-house.md` | Master one-page house template |
| `templates/channel-variant-rules.md` | Per-channel character limits + voice notes |
| `templates/proof-point-schema.md` | Evidence types accepted as proof points |
| `templates/brand-voice-checklist.md` | Tone consistency checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/variant-generator.py` | Generate channel variants from a pillar | Pre-launch copy gen |
| `scripts/tone-drift-detector.py` | Compare variants vs brand voice | Pre-publish |
| `scripts/proof-point-link-checker.py` | Verify proof point URLs / asset references resolve | Pre-publish |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodology: `launch-day-warroom-template`, `launch-retro-template`
- external: [April Dunford, Obviously Awesome](https://www.aprildunford.com/) · [Messaging house framework (Andy Raskin)](https://medium.com/the-mission/the-greatest-sales-deck-ive-ever-seen-4f4ef3391ba0)
