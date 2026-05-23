---
slug: growth-webinar-delivery
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a webinar-delivery runbook artefact (engagement + time-limited offer + 5-email follow-up + repurpose plan) gated by camera-on + offer-during-Q&A rules."
content_id: "82b9ff50f0a6597b"
complexity: deep
produces: spec
est_tokens: 4900
tags: ["webinar", "engagement", "offer", "follow-up", "repurpose", "solo"]
---
# Webinar Delivery

## Summary

**One-sentence:** Produces a webinar-delivery runbook artefact (engagement + time-limited offer + 5-email follow-up + repurpose plan) gated by camera-on + offer-during-Q&A rules.

**One-paragraph:** Solo operators deliver webinars audio-only with offer-at-the-end and lose half the audience before the ask. This methodology pins delivery: camera-on, engagement event every ≤7 minutes, time-limited offer surfaced during Q&A, 5-email follow-up over 7 days, and a repurpose pipeline producing ≥10 derivative assets. Output: a webinar runbook spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-webinar-delivery» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Webinar is scheduled with a confirmed agenda.
- Operator can present with camera-on for the full duration.
- ESP supports the 5-email follow-up sequence.

## Skip If (ANY kills it)

- Pure broadcast format with no Q&A or chat capability.
- Operator has no time-limited offer to make during Q&A.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Webinar agenda + slides | deck | presenter |
| Time-limited offer details | doc | marketing |
| 5-email follow-up sequence drafts | ESP drafts | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/growth-webinar-planning` | Upstream planning methodology. |
| `solo/marketing/content-marketer/` | Parent role / operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the webinar-runbook artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-webinar-delivery.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-webinar-delivery.json` | webinar-runbook JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-webinar-delivery.py` | Validate the webinar-runbook artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-webinar-planning]]
- [[growth-email-marketing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
