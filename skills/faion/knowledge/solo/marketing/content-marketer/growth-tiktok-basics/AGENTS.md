---
slug: growth-tiktok-basics
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a TikTok foundation artefact (profile + content pillars + video formats + 3-month ramp plan) gated by pillar specificity and posting cadence."
content_id: "62b9ff50f0a6597b"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["tiktok", "content-pillars", "vertical-video", "solo"]
---
# TikTok Basics for B2B/SaaS

## Summary

**One-sentence:** Produces a TikTok foundation artefact (profile + content pillars + video formats + 3-month ramp plan) gated by pillar specificity and posting cadence.

**One-paragraph:** Solo B2B/SaaS operators post horizontal YouTube reuploads to TikTok and get no reach. This methodology pins the foundation: 3-5 named content pillars, a conversion-line bio, vertical 9:16 ≤60s format, ≥3 of the named formats per month, and a 3-month ramp plan (warm-up / scale / optimise). Output: a TikTok foundation spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-tiktok-basics» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator can commit to ≥3 native vertical shoots per month.
- Operator's audience is on TikTok (consumer or B2B-curious).
- Operator has authority to publish from a brand account.

## Skip If (ANY kills it)

- Operator's audience is exclusively enterprise B2B with no consumer overlap.
- Operator has zero capacity to shoot vertical content.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Content-pillar shortlist (3-5) | doc | operator |
| Brand TikTok account | account URL | ops |
| Conversion destination URL | URL | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-tiktok-strategies` | Downstream advanced playbook layered on this foundation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the tiktok-foundation artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-tiktok-basics.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-tiktok-basics.json` | tiktok-foundation JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-tiktok-basics.py` | Validate the tiktok-foundation artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-tiktok-strategies]]
- [[growth-youtube-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
