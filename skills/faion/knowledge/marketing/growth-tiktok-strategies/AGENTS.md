# Advanced TikTok Strategies

## Summary

**One-sentence:** Produces an advanced TikTok plan artefact (hook bank + cadence + trend ride + funnel) gated by watch-time targets and a tracked conversion path.

**One-paragraph:** Operators with foundation set still post-and-pray, miss trend windows, and never wire an off-platform funnel. This methodology pins the advanced layer: 3-second hook gate, watch-time optimisation over post frequency, 48-hour trend-ride window, named off-platform conversion path, and ≥1 built-in growth loop (reply-as-video / duet / stitch). Output: a TikTok strategy spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-tiktok-strategies» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- TikTok foundation methodology is already applied (pillars + cadence + bio).
- Operator has trend-monitoring ritual (or capacity for 15 min/day).
- Operator can measure off-platform conversions (UTM + analytics).

## Skip If (ANY kills it)

- Foundation methodology not yet in place — apply that first.
- No off-platform funnel to measure conversion against.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pillar + format catalogue | doc | operator |
| Trend monitoring source (TT Trends / industry feeds) | URL list | ops |
| Off-platform funnel definition | doc | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/growth-tiktok-basics` | Upstream foundation methodology. |
| `solo/marketing/content-marketer/` | Parent role / operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the tiktok-strategy artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-tiktok-strategies.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-tiktok-strategies.json` | tiktok-strategy JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-tiktok-strategies.py` | Validate the tiktok-strategy artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-tiktok-basics]]
- [[growth-youtube-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
