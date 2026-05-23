---
slug: growth-newsletter-growth
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a newsletter-growth plan artefact (positioning + lead magnet + form + traffic + referral) gated by a one-sentence positioning lock."
content_id: "22b9ff50f0a6597b"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["newsletter", "list-building", "lead-magnet", "referral", "solo"]
---
# Newsletter Growth

## Summary

**One-sentence:** Produces a newsletter-growth plan artefact (positioning + lead magnet + form + traffic + referral) gated by a one-sentence positioning lock.

**One-paragraph:** Solo operators chase newsletter subscribers without positioning, then watch churn outpace growth. This methodology pins a growth plan: one-sentence positioning (audience + outcome + frequency), lead-magnet paired form, above-fold placement, double opt-in, and at least one referral mechanism. Output: a newsletter-growth-plan spec gated by the positioning lock.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-newsletter-growth» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator runs OR is launching a newsletter.
- Operator owns or can edit the destination web property.
- Operator has ≥1 newsletter draft to seed the welcome with.

## Skip If (ANY kills it)

- No identified audience — pre-positioning work.
- No web property to host signup form.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| One-sentence positioning candidate | doc | operator |
| Lead-magnet asset | PDF / template | marketing drive |
| Destination signup page wireframe | image / Figma | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-email-marketing` | Downstream consumer of the growing list. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the newsletter-growth-plan artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-newsletter-growth.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-newsletter-growth.json` | newsletter-growth-plan JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-newsletter-growth.py` | Validate the newsletter-growth-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-email-marketing]]
- [[growth-podcast-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
