---
slug: messaging-house-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a 1-page messaging house artefact (root value statement + 3 pillars + proof points + per-channel variants) gated by evidence completeness per pillar."
content_id: "5e69dfa10d71ee06"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["messaging", "positioning", "launch", "pillars", "proof-points", "channel-variants", "solo"]
---
# Messaging House Template

## Summary

**One-sentence:** Produces a 1-page messaging house artefact (root value statement + 3 pillars + proof points + per-channel variants) gated by evidence completeness per pillar.

**One-paragraph:** Teams lack a single artifact connecting positioning to per-channel copy, so launch copy diverges and buyers hear different value props from each channel. This methodology pins a messaging house: one root value statement, exactly 3 pillars, each pillar carries 2-4 evidenced proof points, and each pillar produces per-channel variants (X tweet / LinkedIn post / email subject / ad copy / landing-page hero). Output: a 1-page house artefact owned by a single named owner.

**Ефективно для:**

- готова основа для повторюваної задачі «messaging-house-template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Product has ≥1 confirmed positioning statement OR is preparing for major launch.
- Launch involves ≥3 channels OR a launch sequence ≥2 weeks long.
- ≥6 evidence items available for proof points.

## Skip If (ANY kills it)

- Pre-positioning stage — finish JTBD / value-prop design first.
- Single-tweet launch with no follow-up content — overhead beats payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Root value statement candidate | 1 sentence | operator |
| Pillar candidate list (≥3) | doc | operator |
| Evidence pool (data / quotes / demos) | doc / spreadsheet | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/launch-retro-template` | Downstream retro consumes the house for messaging-fit assessment. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the messaging-house artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/messaging-house-template.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/messaging-house-template.json` | messaging-house JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-messaging-house-template.py` | Validate the messaging-house artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[launch-retro-template]]
- [[growth-landing-page-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
